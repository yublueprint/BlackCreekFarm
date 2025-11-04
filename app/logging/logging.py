import datetime
import os
import gc

#from memory_profiler import profile

# Making it so that it can do both files, whichever gets passed in.
def rotate_if_needed(filename, max_bytes, backup_count):
    if (
            os.path.exists(filename)
            and os.path.getsize(filename) >= max_bytes
        ):
            for i in range(backup_count, 0, -1):
                backup_file = f"{filename}.{i}"
                prev_file = f"{filename}.{i-1}" if i > 1 else filename
                if os.path.exists(prev_file):
                    os.rename(prev_file, backup_file)

def formatLine(line_given):
    """
    Formats line for retrieve_recent_activities function in logging.py

    LINE FORMAT TO GIVE
    -------------------
    Format : YEAR-MONTH-DAY HOUR:MINUTE:SECOND User {user name} {action} {location}: {object name}
    Example : "2025-11-02 16:09:38 User ryan deleted supply: Test Supply C"
    """
    class activityObject:
            def __init__(self, activity, location, user, time):
                self.activity = activity
                self.location = location
                self.user = user
                self.time = time

            def __str__(self):
                return f"Activity: {self.activity}, Location: {self.location}, User: {self.user}, Time: {self.time}"

    chars_to_remove = ["[","]"]

    for char in chars_to_remove:
        line_given = line_given.replace(char, "")

    line_given = line_given.split()

    the_activity = " ".join(line_given[2:])
    the_location = (line_given[5].capitalize())[:-1]
    the_user = line_given[3]
    the_time = " ".join(line_given[0:2])

    line_object = activityObject(the_activity, the_location, the_user, the_time)

    return line_object

class Logger:
    def __init__(self, filename="app.log", modifications_filename="modification_activities.log", max_bytes=1024 * 1024, first_backup_count=3, second_backup_count=3):
        self.filename = filename
        # modification_activites.log file MUST be in the same directory as app.log. Unless we should put modification_activites.log in the instantiation of Logger of all other files.
        self.modifications_filename = os.path.dirname(filename) + "/" + modifications_filename
        self.max_bytes = max_bytes
        self.first_backup_count = first_backup_count
        self.second_backup_count = second_backup_count

    def log(self, message):
        rotate_if_needed(self.filename, self.max_bytes, self.first_backup_count)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

        if ("added" in message) or ("edited" in message) or ("deleted" in message):
            rotate_if_needed(self.modifications_filename, self.max_bytes, self.second_backup_count)
            with open(self.modifications_filename, "a") as f:
                f.write(f"[{timestamp}] {message}\n")

    #@profile
    def retrieve_recent_activity(self, amount_to_retrieve=5, get_all=False):
        """
        Memory and speed efficient way of retrieving recent activity.

        Parameters
        ----------
        amount_to_retrieve : (integer) most recent number of activities to retrieve. Set to 5 by default.
        get_all : (boolean) get all activities or not. False by default.
        chunk_size : (integer) number of bytes to iterate through. 4096 by default.

        Returns
        -------
        An array of recent activities.
        """
        
        #NOTES:
        # When loading an entire 1MB log file, it will always have high memory usage no matter which way you implement it.
        # Time is actually better using readlines and just going through it reversed. Even though it is O(n^2), even at worst case it loads really fast (at most 2 seconds), so time is not to worry here.
        # Now I just gotta find out how to free the memory when entering new page.
        # Solutions I found for the memory problem are...
        # * Force refresh the page. When you click the browser refresh page, the memory drops back to normal baselines. Whereas if you go on another page when on the full recent activities list, it will keep the previous session from the previous page in memory. We have to free that.
        # * Find out how to make Django free all memory when entering a new page ALWAYS.

        recent_activity_array = []

        try:
            gc.collect()

            with open(self.modifications_filename, "r") as f:
                lines = f.readlines()

                for line in reversed(lines):
                    recent_activity_array.append(formatLine(line))
                    if (not get_all and len(recent_activity_array) >= amount_to_retrieve):
                        break

                del lines
                    

        except Exception as e:
            full_error_message = f"Error: {e}"
            # print(full_error_message)
            Logger.log(full_error_message)
        finally:
            # The line below made HUGE improvement to memory. Makes memory drop bac kto baseline after exiting full list page.
            gc.collect()
            return recent_activity_array