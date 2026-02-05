import datetime
import gc
import glob
import os


class activityObject:
    def __init__(self, activity, location, user, time):
        self.activity = activity
        self.location = location
        self.user = user
        self.time = time

    def __str__(self):
        return (
            f"Activity: {self.activity}, Location: {self.location}, "
            f"User: {self.user}, Time: {self.time}"
        )


class Logger:
    def __init__(
        self,
        filename="app.log",
        modifications_filename="modification_activities.log",
        max_bytes=1024 * 1024,
        first_backup_count=3,
        second_backup_count=3,
    ):
        # Might need to use os path here.
        # self.filename = filename
        # print(f"MUST READ: {self.filename}")
        self.logging_directory = "app/logging/"
        self.modification_logs_directory = self.logging_directory + "modification_logs"
        self.modifications_filename = (
            self.modification_logs_directory + "/" + modifications_filename
        )
        self.filename = self.logging_directory + "app_logs/" + "app.log"
        self.max_bytes = max_bytes
        self.first_backup_count = first_backup_count
        self.second_backup_count = second_backup_count

    @staticmethod
    def __rotate_if_needed(filename, max_bytes, backup_count):
        if os.path.exists(filename) and os.path.getsize(filename) >= max_bytes:
            for i in range(backup_count, 0, -1):
                backup_file = f"{filename}.{i}"
                prev_file = f"{filename}.{i - 1}" if i > 1 else filename
                if os.path.exists(prev_file):
                    os.rename(prev_file, backup_file)

    @staticmethod
    def __formatLine(line_given):
        """
        Formats line for retrieve_recent_activities function in logging.py.

        LINE FORMAT TO GIVE
        -------------------
        Format: YEAR-MONTH-DAY HOUR:MINUTE:SECOND User {user name} {action} {location}: {object}
        Example: "2025-11-02 16:09:38 User ryan deleted supply: Test Supply C"
        """
        chars_to_remove = ["[", "]"]
        for char in chars_to_remove:
            line_given = line_given.replace(char, "")

        line_given = line_given.split()
        the_activity = " ".join(line_given[2:])
        the_location = (line_given[5].capitalize())[:-1]
        the_user = line_given[3]
        the_time = " ".join(line_given[0:2])

        line_object = activityObject(the_activity, the_location, the_user, the_time)
        return line_object

    def log(self, message):
        Logger.__rotate_if_needed(
            self.filename, self.max_bytes, self.first_backup_count
        )

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.filename, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

        if ("added" in message) or ("edited" in message) or ("deleted" in message):
            Logger.__rotate_if_needed(
                self.modifications_filename,
                self.max_bytes,
                self.second_backup_count,
            )
            with open(self.modifications_filename, "a") as f:
                f.write(f"[{timestamp}] {message}\n")

    def retrieve_recent_activity(self, amount_to_retrieve=5, get_all=False):
        """
        Memory and speed efficient way of retrieving recent activity.

        Parameters
        ----------
        amount_to_retrieve : int
            Most recent number of activities to retrieve. Default is 5.
        get_all : bool
            Whether to retrieve all activities. Default is False.

        Returns
        -------
        list
            Array of recent activity objects.
        """
        recent_activity_array = []

        try:
            gc.collect()

            with open(self.modifications_filename, "r") as f:
                lines = f.readlines()

                for line in reversed(lines):
                    recent_activity_array.append(Logger.__formatLine(line))
                    if not get_all and len(recent_activity_array) >= amount_to_retrieve:
                        break

                del lines

        except Exception as e:
            full_error_message = f"Error: {e}"
            Logger.log(full_error_message)

        finally:
            # Free memory after reading lines
            gc.collect()
            return recent_activity_array

    def download_all_activity_logs(self):
        folder_path = self.modification_logs_directory
        search_word = "modification_activities"

        search_pattern = os.path.join(folder_path, f"*{search_word}*.log")
        matching_files = glob.glob(search_pattern)

        return matching_files
