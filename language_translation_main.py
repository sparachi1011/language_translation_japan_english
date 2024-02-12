from mhi_logs_translation_imports import *


def LastNlines(syslog_file_path, read_last_n_lines):
    try:
        # assert statement check
        # a condition
        assert read_last_n_lines >= 0

        # declaring variable
        # to implement
        # exponential search
        pos = read_last_n_lines + 1

        # list to store
        # last N lines
        lines = []

        # opening file using with() method
        # so that file get closed
        # after completing work
        with open(syslog_file_path, "r", encoding="utf-8", errors="backslashreplace") as f:

            # loop which runs
            # until size of list
            # becomes equal to N
            while len(lines) <= read_last_n_lines:

                # try block
                try:
                    # moving cursor from
                    # left side to
                    # pos line from end
                    f.seek(-pos, 2)

                # exception block
                # to handle any run
                # time error
                except IOError:
                    f.seek(0)
                    break

                # finally block
                # to add lines
                # to list after
                # each iteration
                finally:
                    lines = list(f)

                # increasing value
                # of variable
                # exponentially
                pos *= 2

        # returning the
        # whole list
        # which stores last
        # N lines
        return lines[-read_last_n_lines:]
    except Exception as e:
        logger.error(
            "Got error in LastNlines function with error:{}".format(e))


def syslog_reading(read_last_n_lines):
    # This function reads the logs inside syslog file
    """
    This Function will read the logs which is located inside syslog.

    Parameters
    ----------

    Returns
    -------
    Updated syslog enteries for every 5 minutes.

    """
    try:
        last_one_day_logs = []
        start_time = datetime.now()
        day_ago_dt = datetime.strptime(day_ago, "%b %d %H:%M:%S")
        now_dt = datetime.strptime(now, "%b %d %H:%M:%S")
        # pdb.set_trace()
        # encoding="utf-8", errors="backslashreplace"
        # with open(syslog_file_path, "rb", ) as log_file:
        #     log_file.seek(-35, 2)
        # lines = LastNlines(syslog_file_path, read_last_n_lines)
        with open(syslog_file_path, "r", encoding='utf-8', errors="backslashreplace") as log_file:
            # for line in (log_file.readlines()[-read_last_n_lines:]):
            lines = log_file.readlines()
            lines = list(set(lines))
        if lines:
            for line in lines:
                if int(line.split()[1]) < 10:
                    d = line.split()[0] + '  ' + \
                        line.split()[1] + ' ' + line.split()[2]
                else:
                    d = line.split()[0] + ' ' + \
                        line.split()[1] + ' ' + line.split()[2]
                log_start_datetime = datetime.strptime(d, "%b %d %H:%M:%S")
                strf_tim = log_start_datetime.strftime("%b %d %H:%M:%S")
                strf_tim_dt = datetime.strptime(strf_tim, "%b %d %H:%M:%S")

                if strf_tim_dt >= day_ago_dt and strf_tim_dt <= now_dt:
                    last_one_day_logs.append(line.strip())
        else:
            last_one_day_logs = [
                "No New Recent Logs Observed by Python MHI Log360 Application."]

        end_time = datetime.now()
        difference = end_time - start_time
        seconds = difference.total_seconds()
        minutes = seconds / 60
        logger.info("Python Script has Submitted with Process ID of {} on Chunk of {} ".format(
            os.getpid(), round(minutes, 3)))

        print('time taken by syslog_reading() in minutes: ', round(minutes, 3))
        print("total records: ", len(last_one_day_logs))

        logger.info('Total number of recent logs found in a syslog file from past 5 minutes: {}.'.format(
            len(last_one_day_logs)))
        return last_one_day_logs
    except Exception as e:
        logger.error(
            "Got error in syslog_reading function with error:{}".format(e))


def log_clensing(sample_str):
    try:
        sample_str = sample_str.lower()
        sample_str = sample_str.replace("#011", "")
        sample_str = sample_str.replace("# 011", "")
        sample_str = sample_str.replace("# 011 ", "")
        sample_str = sample_str.replace("#011 ", "")
        event_timestamp = datetime.strptime(
            sample_str[:15].strip(), "%b %d %H:%M:%S")
        event_timestamp = event_timestamp.strftime("%b %d %H:%M:%S")
        parser_dict = {'event_timestamp': event_timestamp}
        sample_str = sample_str.replace(sample_str[:15], "")

        parser_dict |= {'source_ip': sample_str.split("[", 1)[0].strip()}
        sample_str = sample_str.replace(parser_dict['source_ip'], "", 1)
        parser_dict |= {'event_log': sample_str.split(". ", 1)[0].strip()}
        sample_str = sample_str.replace(" :", ":").strip()
        sample_str = sample_str.replace(
            sample_str.split("[", 1)[0], "", 1).strip()
        sample_str = sample_str.replace(
            sample_str.split(". ", 1)[0], "").strip()
        sample_str = sample_str.replace(". ", "", 1).strip()
        sample_str = sample_str.replace("subject:", "", 1).strip()
        sample_str = sample_str.replace(
            "application information:", "", 1).strip()
        sample_str = sample_str.replace("network information:", "", 1).strip()
        sample_str = sample_str.replace("filter information:", "", 1).strip()
        sample_str = sample_str.replace("process information:", "", 1).strip()
        sample_str = sample_str.replace(
            "target account:", "target account", 1).strip()
        sample_str = sample_str.replace(
            " .exe", ".exe").replace(". exe", ".exe").strip()
        sample_str = sample_str.replace("tesource attribute:-", "", 1).strip()
        sample_str = sample_str.replace("object:", "", 1).strip()

        # sample_str = sample_str.replace("Source address:", "", 1).strip()

        sample_str = sample_str.replace(" : ", ":").replace(
            ": ", ":").replace(" :", ":").strip()
        sample_str = sample_str.replace(": ", ":").strip()
        sample_str = sample_str.replace(
            "access request information:", "", 1).strip()

        return sample_str, parser_dict
    except Exception as e:
        logger.error(
            "Got error in log_clensing function with error:{}".format(e))


def parse_to_json_object(tab_split, parser_dict):
    try:
        tab_split = tab_split.split("  ")
        # pattern = r'(?=\S|^)(.+?):(\S+)'
        pattern = r'(?=\S|^)(.+?):(\S*)'

        regx_results = []

        for elm in tab_split:
            if elm.count(":") == 1:
                elm = elm.split(":")[0]+":"+elm.split(":")[1].replace(" ", "_")
            matches = re.findall(pattern, elm)
            matche = tuple(tuple("_".join(i.split())
                                 for i in a) for a in matches)
            regx_results.extend(matche)

        # Construct dictionary from matches
        output_dict = {}
        current_dict = output_dict
        for key, value in regx_results:
            if key not in current_dict:
                current_dict[key] = value
            else:
                # If key already exists, create new key by appending _other to dup key and update its values
                if not isinstance(current_dict[key], dict):
                    current_dict[key+"_other"] = current_dict[key]
                # current_dict[key+"_other"].update(value)

        parser_dict |= current_dict

        return parser_dict
    except Exception as e:
        logger.error(
            "Got error in parse_to_json_object function with error:{}".format(e))


def translate_jp_to_en(sys_logs_chunk, converted_file_path):
    try:
        print("Python Script has Submitted with Process ID of {} on Chunk of {} ".format(
            os.getpid(), len(sys_logs_chunk)))

        logger.info("Python Script has Submitted with Process ID of {} on Chunk of {} ".format(
            os.getpid(), len(sys_logs_chunk)))

        unique_logs = []

        # Google Translator Package start
        translator = Translator()
        if len(sys_logs_chunk) <= 200:
            try:
                translation = translator.translate(sys_logs_chunk)
                unique_logs = [trans.text.strip() for trans in translation]
            except Exception as e:
                try:
                    translation = translator.translate(sys_logs_chunk)
                    unique_logs = [trans.text.strip() for trans in translation]
                except Exception as e:
                    pass
        else:
            sys_logs_tiny = [sys_logs_chunk[x:x+200]
                             for x in range(0, len(sys_logs_chunk), 200)]
            for tiny_syslog in sys_logs_tiny:
                try:
                    translation = translator.translate(tiny_syslog)
                    unique_logs.extend([trans.text.strip()
                                        for trans in translation])

                except Exception as e:
                    try:
                        translation = translator.translate(tiny_syslog)
                        unique_logs.extend([trans.text.strip()
                                            for trans in translation])
                    except Exception as e:
                        pass
        # Google Translator Package end

        # # Deep Translator Package start
        # for element in sys_logs_chunk:
        #     translation = GoogleTranslator(
        #         source='auto', target='en').translate(element)
        #     unique_logs.append(translation.strip())
        # # Deep Translator Package end

        print("Translation Process Ended by Process ID : {} at {}".format(
            os.getpid(), datetime.now()))

        try:
            with open(converted_file_path, 'r') as file:
                existing_data = json.load(file)
            total_keys = len(existing_data)+1

        except Exception:
            total_keys = 1
            existing_data = {}

        for u_log in unique_logs:
            tab_split, parser_dict = log_clensing(u_log)
            parser_dict = parse_to_json_object(tab_split, parser_dict)
            new_key = str(total_keys)
            existing_data[new_key] = parser_dict
            total_keys += 1

        update_converted_log_file(existing_data, converted_file_path)

    except Exception as e:
        # print("Error at translate_jp_to_en ", e)
        logger.error(
            "Got error in translate_jp_to_en function with error:{}".format(e))


def logs_translation():
    """
    This Function will translates the japanese logs and exclude the duplicates.

    Parameters
    ----------

    Returns
    -------
    Translated List object.

    """
    try:

        start_time = datetime.now()
        sys_logs = syslog_reading(read_last_n_lines)
        if sys_logs:
            def divide_chunks(l, n):
                # looping till length l
                for i in range(0, len(l), n):
                    yield l[i:i + n]
            # decimal = math.modf(len(sys_logs)/5)
            n = math.ceil(len(sys_logs)/5)
            sys_logs = list(divide_chunks(sys_logs, n))
            # translate_jp_to_en(sys_logs[0], converted_file_path)

            def trigger_mutli_process():
                print("\nStart of MultiProcess Execution Mode: ", datetime.now())
                logger.info(
                    "Start of MultiProcess Execution Mode: {}".format(datetime.now()))
                p1 = multiprocessing.Process(
                    target=translate_jp_to_en, args=(sys_logs[0], converted_file_path))
                p2 = multiprocessing.Process(
                    target=translate_jp_to_en, args=(sys_logs[1], converted_file_path))
                p3 = multiprocessing.Process(
                    target=translate_jp_to_en, args=(sys_logs[2], converted_file_path))
                p4 = multiprocessing.Process(
                    target=translate_jp_to_en, args=(sys_logs[3], converted_file_path))
                p5 = multiprocessing.Process(
                    target=translate_jp_to_en, args=(sys_logs[4], converted_file_path))

                p1.start()
                p2.start()
                p3.start()
                p4.start()
                p5.start()
                p1.join()
                p2.join()
                p3.join()
                p4.join()
                p5.join()
            trigger_mutli_process()

        end_time = datetime.now()
        difference = end_time - start_time
        print("\nEnd of MultiProcess Execution Mode: ", difference)
        logger.info(
            "End of MultiProcess Execution Mode: at {} and total time consumed {} ".format(datetime.now(), difference))

    except Exception as e:
        logger.error(
            "Got error in logs_translation function with error:{}".format(e))


def update_converted_log_file(existing_data, converted_file_path):
    """
    This Function append the unique translated logs to converted_file_path.
    Also, if file gets older than 7 days it will remove the old file and new file will get generated

    Parameters
    ----------

    Returns
    -------
    Append the data to a trasnlated log file.

    """
    try:
        start_time = datetime.now()

        try:

            with open(converted_file_path, 'w', encoding='utf-8') as converted_file:
                converted_file.write(json.dumps(existing_data, indent=4))
                converted_file.close()

            # print("Appended to JSON file by Process ID : {} at {}".format(
            #     os.getpid(), datetime.now()))

            logger.info(
                'Appended all the translated unique logs into converted_file.')
        except Exception as e:
            logger.error(
                "Got error in update_converted_log_file function with error:{}".format(e))
            converted_file.close()

        end_time = datetime.now()
        difference = end_time - start_time
        print('time taken by update_converted_log_file() in minutes: ',
              difference)
        logger.info(
            "time taken by update_converted_log_file() in minutes: {}".format(difference))

    except Exception as e:
        logger.error(
            "Got error in update_converted_log_file function with error:{}".format(e))


def check_file_exist(days_to_keep=7):
    """
    This Function will check all the file are available or not.

    Parameters
    ----------
    days_to_keep : Integer
        DESCRIPTION: For how many days the converted file path exist.


    Returns
    -------
    Returns all the file available status

    """
    try:
        start_time = datetime.now()
        current_time = datetime.now()
        datetime_7_days_old = current_time - timedelta(days=7)
        converted_file_path = working_directory + 'mhi_translated_logs/mhi_translated_logs_' + \
            datetime_7_days_old.strftime("%Y_%m_%d") + '.json'

        # checking syslog_file_path
        try:
            if os.path.isfile(syslog_file_path):
                syslog_file_exists = True
            else:
                syslog_file_exists = False

        except Exception as e:
            logger.error(
                "Got issue with syslog_file_path, please check if it exists also refer error:{}".format(e))

        # # checking script execution log mhi_log_file_path
        # try:
        #     if os.path.exists(working_directory+mhi_log_directory_name):
        #         if os.path.isfile(mhi_log_file_path):
        #             mhi_log_file_exists = True
        #         # else:
        #         #     with open(mhi_log_file_path, 'a', encoding='utf-8'):
        #         #         mhi_log_file_exists = True
        #     else:
        #         os.mkdir(os.path.join(working_directory,mhi_log_directory_name))
        #         with open(mhi_log_file_path, 'a', encoding='utf-8'):
        #                 mhi_log_file_exists = True

        # except Exception as e:
        #     logger.error("Got issue with mhi_log_file_path, so creating new mhi log file:{}".format(e))
        #     mhi_log_file_exists = False

        # checking converted_file_path
        try:
            if os.path.exists(converted_file_path.rsplit("/", 1)[0]):
                if os.path.isfile(converted_file_path):
                    age = current_time - datetime_7_days_old
                    # print(f'age of a file is: {age.days}')
                    if age.days >= days_to_keep:
                        logger.info(
                            "converted_file_path gets deleted every 7 days, so creating new converted file")
                        log_file = open(converted_file_path,
                                        'a', encoding='utf-8')
                        log_file.close()

                else:
                    logger.info(
                        "converted_file_path doesn't existed, so creating new converted file")
                    log_file = open(converted_file_path, 'a', encoding='utf-8')
                    log_file.close()
                converted_file_exists = True
            else:
                os.mkdir(converted_file_path.rsplit("/", 1)[0])
                log_file = open(converted_file_path, 'a')
                log_file.close()
            converted_file_exists = True

        except Exception as e:
            logger.error('issue with converted_file_path {}'.format(e))
            converted_file_exists = False
        end_time = datetime.now()
        difference = end_time - start_time
        seconds = difference.total_seconds()
        minutes = seconds / 60
        print('time taken by check_file_exist() in minutes: ', round(minutes, 3))
        return syslog_file_exists, converted_file_exists, converted_file_path
    except Exception as e:
        logger.error(
            "Got error in check_file_exist function with error:{}".format(e))


if __name__ == "__main__":
    start_time = datetime.now()
    read_last_n_lines = 500
    syslog_file_exists, converted_file_exists, converted_file_path = check_file_exist(
        days_to_keep=7)

    if syslog_file_exists and converted_file_exists:
        logs_translation()

    else:
        print(syslog_file_exists, converted_file_exists, converted_file_path)

    end_time = datetime.now()
    difference = end_time - start_time
    print('Total Time Taken by Whole Process to Complete in minutes: ', difference)
