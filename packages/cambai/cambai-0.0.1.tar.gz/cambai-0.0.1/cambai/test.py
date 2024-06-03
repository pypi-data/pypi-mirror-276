from dotenv import load_dotenv
from cambai import CambAI
# from rich import print
from rich.table import Table
import json

load_dotenv()

camb = CambAI()
# table = Table(show_header=True, header_style="bold magenta")
# print(camb.dubbing)

print(camb.get_languages("source", True))

response = camb.get_dubbed_run_info(11304)

# print(response["video_url"])


# table.add_column("Type")
# table.add_column("URL", width=80)

# for key, value in response.items():
#     table.add_row(key, value)

# print(table)

# print(camb.get_languages("source"))
