#!make

include .env

M = $(shell printf "\033[34;1m▶\033[0m")

arg_test: ; $(info $(M) Testing...)
	echo args were: foo: $(foo) bar: $(bar)

#-------------------------------------------------------------------------------
# PRODUCTION
#-------------------------------------------------------------------------------

set_prod_env: ; $(info $(M) Setting production env vars...)
	heroku config:set DATABASE_URL=$(PROD__DATABASE_URL) --remote production
	heroku config:set DEBUG=$(PROD__DEBUG) --remote production
	heroku config:set ALL_AUTH_EMAIL_USE_TLS=$(PROD__ALL_AUTH_EMAIL_USE_TLS) --remote production
	heroku config:set ALL_AUTH_EMAIL_HOST=$(PROD__ALL_AUTH_EMAIL_HOST) --remote production
	heroku config:set ALL_AUTH_EMAIL_PORT=$(PROD__ALL_AUTH_EMAIL_PORT) --remote production
	heroku config:set ALL_AUTH_DEFAULT_FROM_EMAIL=$(PROD__ALL_AUTH_DEFAULT_FROM_EMAIL) --remote production
	heroku config:set ALL_AUTH_EMAIL_HOST_USER=$(PROD__ALL_AUTH_EMAIL_HOST_USER) --remote production
	heroku config:set ALL_AUTH_EMAIL_HOST_PASSWORD=$(PROD__ALL_AUTH_EMAIL_HOST_PASSWORD) --remote production
	heroku config:set DISABLE_COLLECTSTATIC=$(PROD__DISABLE_COLLECTSTATIC) --remote production
	heroku config:set SECRET_KEY=$(PROD__SECRET_KEY) --remote production
	heroku config:set WEBAPP_URL=$(PROD__WEBAPP_URL) --remote staging
	heroku config:set TIMES=$(PROD__TIMES) --remote production

deploy_production: set_prod_env ; $(info $(M) Running staging server...)
	git push production master
	heroku run python manage.py migrate --app $(PRODVAR---HEROKU_APP_NAME)

create_production_superuser: set_staging_env; $(info $(M) Creating super-user on production server...)
	heroku run python3 manage.py createsuperuser --app $(PRODVAR---HEROKU_APP_NAME)

#-------------------------------------------------------------------------------
# STAGING 
#-------------------------------------------------------------------------------

set_staging_env: ; $(info $(M) Setting staging env vars...)
	heroku config:set DATABASE_URL=$(STAGE__DATABASE_URL) --remote staging
	heroku config:set DEBUG=$(STAGE__DEBUG) --remote staging
	heroku config:set ALL_AUTH_EMAIL_USE_TLS=$(STAGE__ALL_AUTH_EMAIL_USE_TLS) --remote staging
	heroku config:set ALL_AUTH_EMAIL_HOST=$(STAGE__ALL_AUTH_EMAIL_HOST) --remote staging
	heroku config:set ALL_AUTH_EMAIL_PORT=$(STAGE__ALL_AUTH_EMAIL_PORT) --remote staging
	heroku config:set ALL_AUTH_DEFAULT_FROM_EMAIL=$(STAGE__ALL_AUTH_DEFAULT_FROM_EMAIL) --remote staging
	heroku config:set ALL_AUTH_EMAIL_HOST_USER=$(STAGE__ALL_AUTH_EMAIL_HOST_USER) --remote staging
	heroku config:set ALL_AUTH_EMAIL_HOST_PASSWORD=$(STAGE__ALL_AUTH_EMAIL_HOST_PASSWORD) --remote staging
	heroku config:set DISABLE_COLLECTSTATIC=$(STAGE__DISABLE_COLLECTSTATIC) --remote staging
	heroku config:set SECRET_KEY=$(STAGE__SECRET_KEY) --remote staging
	heroku config:set WEBAPP_URL=$(STAGE__WEBAPP_URL) --remote staging
	heroku config:set TIMES=$(STAGE__TIMES) --remote staging

deploy_staging: set_staging_env; $(info $(M) Running staging server...)
	git push staging master
	heroku run python manage.py migrate --app $(STAGEVAR---HEROKU_APP_NAME)

create_staging_superuser: set_staging_env; $(info $(M) Creating super-user on staging server...)
	heroku run python3 manage.py createsuperuser --app $(STAGEVAR---HEROKU_APP_NAME)

#-------------------------------------------------------------------------------
# LOCAL
#-------------------------------------------------------------------------------

run_local: ; $(info $(M) Running local server...)
	env \
		DATABASE_URL=$(DATABASE_URL) \
		DEBUG=$(DEBUG) \
		ALL_AUTH_EMAIL_USE_TLS=$(ALL_AUTH_EMAIL_USE_TLS) \
		ALL_AUTH_EMAIL_HOST=$(ALL_AUTH_EMAIL_HOST) \
		ALL_AUTH_EMAIL_PORT=$(ALL_AUTH_EMAIL_PORT) \
		ALL_AUTH_DEFAULT_FROM_EMAIL=$(ALL_AUTH_DEFAULT_FROM_EMAIL) \
		ALL_AUTH_EMAIL_HOST_USER=$(ALL_AUTH_EMAIL_HOST_USER) \
		ALL_AUTH_EMAIL_HOST_PASSWORD=$(ALL_AUTH_EMAIL_HOST_PASSWORD) \
		DISABLE_COLLECTSTATIC=$(DISABLE_COLLECTSTATIC) \
		SECRET_KEY=$(SECRET_KEY) \
		WEBAPP_URL=$(WEBAPP_URL) \
		TIMES=$(TIMES) \
		python3 manage.py runserver 0.0.0.0:5002

migrate_local_db: ; $(info $(M) Migrating local database...)
	env \
		DATABASE_URL=$(DATABASE_URL) \
		DEBUG=$(DEBUG) \
		ALL_AUTH_EMAIL_USE_TLS=$(ALL_AUTH_EMAIL_USE_TLS) \
		ALL_AUTH_EMAIL_HOST=$(ALL_AUTH_EMAIL_HOST) \
		ALL_AUTH_EMAIL_PORT=$(ALL_AUTH_EMAIL_PORT) \
		ALL_AUTH_DEFAULT_FROM_EMAIL=$(ALL_AUTH_DEFAULT_FROM_EMAIL) \
		ALL_AUTH_EMAIL_HOST_USER=$(ALL_AUTH_EMAIL_HOST_USER) \
		ALL_AUTH_EMAIL_HOST_PASSWORD=$(ALL_AUTH_EMAIL_HOST_PASSWORD) \
		DISABLE_COLLECTSTATIC=$(DISABLE_COLLECTSTATIC) \
		SECRET_KEY=$(SECRET_KEY) \
		WEBAPP_URL=$(WEBAPP_URL) \
		TIMES=$(TIMES) \
		python3 manage.py migrate

make_local_migrations: ; $(info $(M) Migrating local database...)
	env \
		DATABASE_URL=$(DATABASE_URL) \
		DEBUG=$(DEBUG) \
		ALL_AUTH_EMAIL_USE_TLS=$(ALL_AUTH_EMAIL_USE_TLS) \
		ALL_AUTH_EMAIL_HOST=$(ALL_AUTH_EMAIL_HOST) \
		ALL_AUTH_EMAIL_PORT=$(ALL_AUTH_EMAIL_PORT) \
		ALL_AUTH_DEFAULT_FROM_EMAIL=$(ALL_AUTH_DEFAULT_FROM_EMAIL) \
		ALL_AUTH_EMAIL_HOST_USER=$(ALL_AUTH_EMAIL_HOST_USER) \
		ALL_AUTH_EMAIL_HOST_PASSWORD=$(ALL_AUTH_EMAIL_HOST_PASSWORD) \
		DISABLE_COLLECTSTATIC=$(DISABLE_COLLECTSTATIC) \
		SECRET_KEY=$(SECRET_KEY) \
		WEBAPP_URL=$(WEBAPP_URL) \
		TIMES=$(TIMES) \
		python3 manage.py makemigrations

collect_static : ; $(info $(M) Collecting local static-files...)
	env \
		DATABASE_URL=$(DATABASE_URL) \
		DEBUG=$(DEBUG) \
		ALL_AUTH_EMAIL_USE_TLS=$(ALL_AUTH_EMAIL_USE_TLS) \
		ALL_AUTH_EMAIL_HOST=$(ALL_AUTH_EMAIL_HOST) \
		ALL_AUTH_EMAIL_PORT=$(ALL_AUTH_EMAIL_PORT) \
		ALL_AUTH_DEFAULT_FROM_EMAIL=$(ALL_AUTH_DEFAULT_FROM_EMAIL) \
		ALL_AUTH_EMAIL_HOST_USER=$(ALL_AUTH_EMAIL_HOST_USER) \
		ALL_AUTH_EMAIL_HOST_PASSWORD=$(ALL_AUTH_EMAIL_HOST_PASSWORD) \
		DISABLE_COLLECTSTATIC=$(DISABLE_COLLECTSTATIC) \
		SECRET_KEY=$(SECRET_KEY) \
		WEBAPP_URL=$(WEBAPP_URL) \
		TIMES=$(TIMES) \
		python3 manage.py collectstatic

create_local_superuser: ; $(info $(M) Creating super-user for local server...)
	env \
		DATABASE_URL=$(DATABASE_URL) \
		DEBUG=$(DEBUG) \
		ALL_AUTH_EMAIL_USE_TLS=$(ALL_AUTH_EMAIL_USE_TLS) \
		ALL_AUTH_EMAIL_HOST=$(ALL_AUTH_EMAIL_HOST) \
		ALL_AUTH_EMAIL_PORT=$(ALL_AUTH_EMAIL_PORT) \
		ALL_AUTH_DEFAULT_FROM_EMAIL=$(ALL_AUTH_DEFAULT_FROM_EMAIL) \
		ALL_AUTH_EMAIL_HOST_USER=$(ALL_AUTH_EMAIL_HOST_USER) \
		ALL_AUTH_EMAIL_HOST_PASSWORD=$(ALL_AUTH_EMAIL_HOST_PASSWORD) \
		DISABLE_COLLECTSTATIC=$(DISABLE_COLLECTSTATIC) \
		SECRET_KEY=$(SECRET_KEY) \
		WEBAPP_URL=$(WEBAPP_URL) \
		TIMES=$(TIMES) \
		python3 manage.py createsuperuser 

cli: ; $(info $(M) Running Django CLI with local config...)
	env \
		DATABASE_URL=$(DATABASE_URL) \
		DEBUG=$(DEBUG) \
		ALL_AUTH_EMAIL_USE_TLS=$(ALL_AUTH_EMAIL_USE_TLS) \
		ALL_AUTH_EMAIL_HOST=$(ALL_AUTH_EMAIL_HOST) \
		ALL_AUTH_EMAIL_PORT=$(ALL_AUTH_EMAIL_PORT) \
		ALL_AUTH_DEFAULT_FROM_EMAIL=$(ALL_AUTH_DEFAULT_FROM_EMAIL) \
		ALL_AUTH_EMAIL_HOST_USER=$(ALL_AUTH_EMAIL_HOST_USER) \
		ALL_AUTH_EMAIL_HOST_PASSWORD=$(ALL_AUTH_EMAIL_HOST_PASSWORD) \
		DISABLE_COLLECTSTATIC=$(DISABLE_COLLECTSTATIC) \
		SECRET_KEY=$(SECRET_KEY) \
		WEBAPP_URL=$(WEBAPP_URL) \
		TIMES=$(TIMES) \
		python3 manage.py shell

start_app: ; $(info $(M) Adding new app...)
	env \
		DATABASE_URL=$(DATABASE_URL) \
		DEBUG=$(DEBUG) \
		ALL_AUTH_EMAIL_USE_TLS=$(ALL_AUTH_EMAIL_USE_TLS) \
		ALL_AUTH_EMAIL_HOST=$(ALL_AUTH_EMAIL_HOST) \
		ALL_AUTH_EMAIL_PORT=$(ALL_AUTH_EMAIL_PORT) \
		ALL_AUTH_DEFAULT_FROM_EMAIL=$(ALL_AUTH_DEFAULT_FROM_EMAIL) \
		ALL_AUTH_EMAIL_HOST_USER=$(ALL_AUTH_EMAIL_HOST_USER) \
		ALL_AUTH_EMAIL_HOST_PASSWORD=$(ALL_AUTH_EMAIL_HOST_PASSWORD) \
		DISABLE_COLLECTSTATIC=$(DISABLE_COLLECTSTATIC) \
		SECRET_KEY=$(SECRET_KEY) \
		WEBAPP_URL=$(WEBAPP_URL) \
		TIMES=$(TIMES) \
	python3 manage.py startapp $(app_name)


#-------------------------------------------------------------------------------
# PSQL (Database Command Line) 
#-------------------------------------------------------------------------------

psql_stage: ; $(info $(M) Connecting to staging database...)
	psql $(STAGE__DATABASE_URL)

psql_prod: ; $(info $(M) Connecting to staging database...)
	psql $(PROD__DATABASE_URL)

psql_local: ; $(info $(M) Connecting to local database...)
	psql $(DATABASE_URL)

#-------------------------------------------------------------------------------
# DUMP (Database Dump to File) 
#-------------------------------------------------------------------------------

dump_stage_db: ; $(info $(M) Dumping staging database to local file...)
	rm -f dump.sql
	pg_dump $(STAGE__DATABASE_URL) > dump.sql

dump_prod_db: ; $(info $(M) Dumping production database to local file...)
	rm -f dump.sql
	pg_dump $(PROD__DATABASE_URL) > dump.sql

#-------------------------------------------------------------------------------
# SYNC (Copy Database to Database)
#-------------------------------------------------------------------------------

sync_db_staging_from_prod: dump_prod_db ; $(info $(M) Syncing staging database with data from production...)
	sed -i '' 's/$(PRODVAR---DATABASE_USER)/$(STAGEVAR---DATABASE_USER)/g' dump.sql
	heroku pg:reset $(STAGEVAR---HEROKU_DATABASE_NAME) \
		--app $(STAGEVAR---HEROKU_APP_NAME) \
		--confirm $(STAGEVAR---HEROKU_APP_NAME) 
	psql $(STAGE__DATABASE_URL) < dump.sql

sync_db_local_from_stage: dump_stage_db ; $(info $(M) Syncing local database with data from staging...)
	psql -c "DROP DATABASE $(LOCALVAR---DATABASE_NAME)"
	psql -c "CREATE DATABASE $(LOCALVAR---DATABASE_NAME)"
	sed -i '' 's/$(STAGEVAR---DATABASE_USER)/$(LOCALVAR---DATABASE_USER)/g' dump.sql
	psql $(LOCALVAR---DATABASE_NAME) < dump.sql

sync_db_local_from_prod: dump_prod_db ; $(info $(M) Syncing local database with data from production...)
	psql -c "DROP DATABASE $(LOCALVAR---DATABASE_NAME)"
	psql -c "CREATE DATABASE $(LOCALVAR---DATABASE_NAME)"
	sed -i '' 's/$(PRODVAR---DATABASE_USER)/$(LOCALVAR---DATABASE_USER)/g' dump.sql
	psql $(LOCALVAR---DATABASE_NAME) < dump.sql

.PHONY: prod_set_env, run_local, local_dump_db
