import datetime
import os


class Logger:
    def __init__(self, filename="app.log", max_bytes=1024 * 1024, backup_count=3):
        self.filename = filename
        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def log(self, message):
        self._rotate_if_needed()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def _rotate_if_needed(self):
        if (
            os.path.exists(self.filename)
            and os.path.getsize(self.filename) >= self.max_bytes
        ):
            for i in range(self.backup_count, 0, -1):
                backup_file = f"{self.filename}.{i}"
                prev_file = f"{self.filename}.{i-1}" if i > 1 else self.filename
                if os.path.exists(prev_file):
                    os.rename(prev_file, backup_file)

    def retrieve_recent_activity(self):

        class activityObject:
            # Examples for Location were North Paddock, East Fields, Barn 2, etc. We will need to dicuss this.
            # Actually, location will just be the type of stock. So like they know where to go.
            def __init__(self, activity, location, user, time):
                self.activity = activity
                self.location = location
                self.user = user
                self.time = time

        recent_activity_array = []
        chars_to_remove = ["[","]"]
        amount_to_retrieve = 3
        count = 0

        try:
            with open(self.filename, 'r') as file:
                all_lines = file.readlines()

                # Starting by the most recent
                for line in reversed(all_lines):
                    # Resetting values each iteration
                    the_activity = ''
                    the_location = ''
                    the_user = ''
                    the_time = ''

                    # Only recent activity to include is add, edit, or deletion.
                    if ("added" in line) or ("edited" in line) or ("deleted" in line):
                        for char in chars_to_remove:
                            line = line.replace(char, "")
                        line = line.split()
                        # print(line)

                        the_activity = " ".join(line[2:])
                        the_location = line[5].replace(":","")
                        the_user = line[3]
                        the_time = " ".join(line[0:2])

                        # Keep for testing
                        # print(the_activity)
                        # print(the_location)
                        # print(the_user)
                        # print(the_time)
                        
                        line_object = activityObject(the_activity, the_location, the_user, the_time)

                        # Keep for testing
                        # print(line_object.activity)
                        # print(line_object.location)
                        # print(line_object.user)
                        # print(line_object.time)

                        recent_activity_array.append(line_object)
                        count = count + 1

                    if count >= amount_to_retrieve:
                        break

        except Exception as e:
            print("Error: " + e)

        finally:
            return recent_activity_array
