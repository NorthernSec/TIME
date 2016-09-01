database_exists=`sudo -u postgres psql -lqt | cut -f 1 -d"|" | grep "nstime" | wc -l`
if [ "$database_exists" == "1" ]
then
  echo "[!] The database 'nstime' already exists."
  echo "[!] Continuing will drop the database and all its content."
  read -p "    > Are you sure? [y/N] " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    sudo -u postgres psql -tAc "DROP DATABASE IF EXISTS NSTIME;"
    database_exists=`sudo -u postgres psql -lqt | cut -f 1 -d"|" | grep "nstime" | wc -l`
    if [ "$database_exists" == "1" ]
    then
      echo "[!] Could not drop the database! Exiting script."
      exit
    fi
  else
    exit
  fi
fi

user_exists=`sudo -u postgres psql -tAc "select 1 from pg_roles where rolname='nstime'"`
if [ "$user_exists" == "1" ]
then
  echo "[!] User 'nstime' already exists. Do you want to delete it?"
  read -p "    > Delete? [y/N] " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    sudo -u postgres psql -tAc "DROP USER NSTIME"
    echo "[v] User dropped"
  else
    echo "[v] Existing user used"
  fi
fi

user_exists=`sudo -u postgres psql -tAc "select 1 from pg_roles where rolname='nstime'"`
if [ "$user_exists" != "1" ]
then
  echo "Please specify a password for user NSTIME:"
  read -s pass1
  echo "Repeat the password:"
  read -s pass2
  if [ "$pass1" != "$pass2" ]
  then
    exit
  fi
  sudo -u postgres psql -tAc "CREATE USER NSTIME WITH PASSWORD '$pass1';"
  echo "[v] User 'nstime' created"
fi

sudo -u postgres psql -tAc "CREATE DATABASE NSTIME OWNER nstime;" > /dev/null
sudo -u postgres psql -d nstime -f TIME/lib/db_model.sql > /dev/null
sudo -u postgres psql -d nstime -f TIME/lib/db_data.sql > /dev/null
sudo -u postgres psql -d nstime -tAc "REVOKE ALL ON DATABASE nstime FROM public;" > /dev/null
sudo -u postgres psql -d nstime -tAc "GRANT  ALL ON DATABASE nstime TO nstime;" > /dev/null
sudo -u postgres psql -d nstime -tAc "GRANT  ALL ON ALL TABLES    IN SCHEMA public TO nstime;" > /dev/null
sudo -u postgres psql -d nstime -tAc "GRANT  ALL ON ALL SEQUENCES IN SCHEMA public TO nstime;" > /dev/null

echo "[v] Database created"

