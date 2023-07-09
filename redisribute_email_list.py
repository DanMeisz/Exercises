from pandas import DataFrame
from os import mkdir,path,getcwd,listdir,remove
from json import load
from shutil import move
from datetime import datetime
from logging import DEBUG,basicConfig,debug,info,exception

#comparing pandas df against JSON file, overwriting the email address in the df if it's different to the JSON file and appending rows that
#are not present in the df
def compare_df(df, json):
    for name, email in json.items():
        first_name, last_name = name.split(" ")
        same_row = df[(df["First Name"] == first_name) & (df["Last Name"] == last_name)]
        if not same_row.empty:
            df_email = same_row["Email Address"].iloc[0]
            if df_email != email:
                df.loc[(df["First Name"]==first_name) & (df["Last Name"] == last_name),"Email Address"] = email
                debug(f"Email mismatch detected: {df_email} overwritten with {email}")
            else:
                debug(f"Matching email found for {name}: {email}")
                debug("The emails match")
        else:
            df = df.append({
                "First Name": first_name,
                "Last Name": last_name,
                "Email Address": email[0]
            }, ignore_index=True)
            debug(f"Email address {email} not found in the df, adding new row.")
    debug(f"Dataframe after conversion: \n {df}")
    return df

#create a new directory if directory with the same name doesn't exist       
def create_dir(dir_name):
        if path.isdir(dir_name) == False:
            mkdir(dir_name)
            info(f"directory {dir_name} has been created")
        else:
            info(f"directory {dir_name} already exist")

#returns today's date as a string
def current_date():
    current_datetime = datetime.today()
    current_date = current_datetime.date()
    debug((f"current_date() function's return value: {current_date}"))
    return str(current_date)

#moves file from current working directory to destination folder
def move_file(file,dstn):
    try:
        src_path = f"{getcwd()}/{file}"
        dst_path = f"{getcwd()}/{dstn}/{file}"
        move(src_path, dst_path)
        info(f"moved from {src_path} to {dst_path}")
    except:
        exception(Exception)
        info("Failure")
        raise Exception

#by extracting the date from the logfile's timestamp we can check whether the log is older than 15 days,if it is we delete it
def chk_log_age():
    log_dir=f"{getcwd()}/log"
    log_list = listdir(log_dir)
    for log in log_list:
        file_path= f"{log_dir}/{log}"
        timestmp =path.getmtime(file_path)
        file_date=datetime.fromtimestamp(timestmp).date()
        date_format ="%Y-%m-%d"
        todays_date = datetime.strptime(current_date(),date_format).date()
        log_age=todays_date-file_date
        log_age=log_age.days
        if log_age >=15:
            info(f"{log} is older than 15 days.")
            try:
                remove(log_dir)
                info(f"{log} removed.")
            except:
                exception(Exception)
                info("Failure")
                raise Exception

#setting up logging
create_dir("log")
log_name=f"{getcwd()}/log/log_{current_date()}.log"

basicConfig(
    filename=log_name,
    level=DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
    filemode='a',
    force=True
    )

#initial list provided
first_name = ["Peter", "Robert", "James", "George", "Frank"] 
last_name = ["Jackson", "Barb", "Samson", "Koval", "Peterson"] 
email_address = ["peter.j@gmail.com", "robert.barb@gmail.com", 
"james.s@gmail.com", "george.k@gmail.com", "frank.p@gmail.com"]
debug(f"\n Lists created:\n first_name: {first_name} \n last_name: {last_name} \n email_address: {email_address}")

#creating a list that can be converted to a pandas df from the initial list provided
user_list = []
debug(f"\n user_list created{user_list}")

for i in range(len(first_name)):
    user_list.append([])
    user_list[i].append(first_name[i])
    user_list[i].append(last_name[i])
    user_list[i].append(email_address[i])
debug(f"\n user_list populated {user_list}")

#converting list to pandas df
df = DataFrame (user_list, columns = ["First Name","Last Name","Email Address"])
debug(f"\n user_list converted to df: \n {df} ")

#compare dataframe against JSON
with open("test.json",encoding="utf-8") as f:
    json = load(f)
df = compare_df(df, json)


#converting pandas df to csv file
csv_name=(f"email_distributed_{current_date()}.csv")
try:
    df.to_csv(csv_name)
except:
    exception(Exception)
    info("Failure")
    raise Exception
debug(f"df \n {df}")
debug(f"df converted to csv file {csv_name}")

create_dir("csv_files")
create_dir("archive")
move_file(csv_name,"archive")
chk_log_age()
#if we reach this point, our runtime was successful
info("Success")
