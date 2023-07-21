dotenv_filler = (
    "# .env initial structure.\n",
    "# Fill with correct data to proper application work.\n",
    "\n",
    "# Django variables\n",
    "\n",
    "DJANGO_SECRET_KEY=\n",
    "\n",
    "# Database variables\n",
    "\n",
    "DATABASE_NAME=\n",
    "DATABASE_USER=\n",
    "DATABASE_PASSWORD=\n",
    "# Metrika variables\n",
    "\n",
    "METRIKA_COUNTER_ID=\n",
    "METRIKA_API_ACCESS_TOKEN=\n",
    "\n",
    "# Topvisor variables\n",
    "\n",
    "TOPVISOR_USER_ID=\n",
    "TOPVISOR_PROJECT_ID=\n",
    "\n",
    "TOPVISOR_API_KEY=\n",
)

try:
    with open(".env", "r") as f:
        if (len(f.read().strip()) > 0):
            raise FileExistsError(
                ".env file already exists and contains data."
            )
        else:
            raise FileNotFoundError()

except FileNotFoundError as e:
    with open(".env", "w") as f:
        f.writelines(dotenv_filler)

except FileExistsError as e:
    print(e)
