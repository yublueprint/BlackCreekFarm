import datetime
import os

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

# Format lines into activityObjects function.
def format_lines(final_lines):
    class activityObject:
            def __init__(self, activity, location, user, time):
                self.activity = activity
                self.location = location
                self.user = user
                self.time = time

    final_result = []
    chars_to_remove = ["[","]"]

    for line in reversed(final_lines):
        the_activity = ''
        the_location = ''
        the_user = ''
        the_time = ''

        for char in chars_to_remove:
            line = line.replace(char, "")
        line = line.split()

        # print(line)

        the_activity = " ".join(line[2:])
        the_location = (line[5].capitalize())[:-1]
        the_user = line[3]
        the_time = " ".join(line[0:2])

        # print(the_activity)
        # print(the_location)
        # print(the_user)
        # print(the_time)

        # Create the activityObject
        line_object = activityObject(the_activity, the_location, the_user, the_time)

        final_result.append(line_object)
    return final_result

class Logger:
    def __init__(self, filename="app.log", modifications_filename="modification_activities.log", max_bytes=1024 * 1024, first_backup_count=3, second_backup_count=3):
        self.filename = filename
        # modification_activites.log file MUST be in the same directory as app.log
        # For some reason and I don't know why, app.log is detected but modification_activites.log isn't, 
        # so I have to do this where I get the pathway.
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

    def retrieve_recent_activity(self, amount_to_retrieve=5, get_all=False, chunk_size=4096):
        recent_activity_array = []

        try:
            with open(self.modifications_filename, 'rb') as f:
                # Go to the end of the file.
                f.seek(0,2)
                file_size = f.tell()

                # Start reading back from the very end.
                position = file_size
                lines = []

                # Loop backward, reading chunks until we have enough lines.
                # (len(lines) < amount_to_retrieve)
                while (position > 0):
                    if ((get_all == False) and (len(lines) > amount_to_retrieve)):
                        break
                    # Calculate where to seek to (start of the chunk).
                    seek_to = max(0, position - chunk_size)

                    # Move the file pointer back.
                    f.seek(seek_to)

                    # Read the chunk of data.
                    chunk = f.read(position - seek_to)

                    # Split the chunk by newlines (b'\n').
                    # Last element usually is an empty string or an incomplete line from the previous chunk.
                    lines_in_chunk = chunk.split(b'\n')

                    # Process lines in the chunk from last to first.
                    # Note: Very last element of the split is either empty (if the file ends with a newline) or the content after the last newline.
                    for line in lines_in_chunk[:-1][::-1]:
                        # Prepend the line to the list.
                        lines.insert(0, line)
                        if ((get_all == False) and (len(lines) == amount_to_retrieve)):
                            break

                    # Update the position for the next iteration.
                    position = seek_to

                # If reached the start of the file (position == 0) and we haven't retrieved the amount of lines we want,
                # the very first element of the chunk (lines_in_chunk[0]) is the start of the file and must be included.
                # and (len(lines) < amount_to_retrieve)
                if (position == 0) and len(lines) < amount_to_retrieve and lines_in_chunk:
                    lines.insert(0, lines_in_chunk[0])

                # Decode and return the final list of lines (trimmed to the amount of lines we want to retrieve).
                # Since we inserted lines at index 0, they are already in correct order.
                if (get_all == False):
                    final_lines = [line.decode('utf-8') for line in lines[-amount_to_retrieve:] if line]
                else:
                    final_lines = [line.decode('utf-8') for line in lines if line]

            # Format the lines we retrieved into activityObjects to be displayed in the dashboard.
            recent_activity_array = format_lines(final_lines)

        except Exception as e:
            full_error_message = f"Error: {e}"
            print(full_error_message)
            Logger.log(full_error_message)
        finally:
            return recent_activity_array