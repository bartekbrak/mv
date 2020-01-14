notatki z przenoszenia slacka na mattermosta

> start slack export, allow time

https://bartekbrak.slack.com/services/export

> get slack exporter

    wget https://github.com/grundleborg/slack-advanced-exporter/releases/download/v0.3.0/slack-advanced-exporter-linux-amd64
    chmod +x slack-advanced-exporter-linux-amd64

> follow docs

https://docs.mattermost.com/administration/migrating.html#migrating-from-slack

> get slack token

https://api.slack.com/custom-integrations/legacy-tokens

    token=xoxp-16083099889-16083793111-???

> export slack

    ./slack-advanced-exporter-linux-amd64 \
        --input-archive your-slack-team-export.zip \
        --output-archive export-with-emails.zip \
        fetch-emails --api-token $token


    ./slack-advanced-exporter-linux-amd64 \
        --input-archive export-with-emails.zip \
        --output-archive export-with-attachments.zip \
        fetch-attachments

    # 2020/01/14 06:48:56 ++++++ file_share post has missing properties on it's File object: 1483437617.000002
    # Downloaded attachment into output archive: FFRA00XFG.
    # ...


    $ ls -hl *zip
    -rw-rw-r-- 1 bartek bartek 3.2G Dec 18 15:40 export-with-attachments.zip
    -rw-rw-r-- 1 bartek bartek  21M Dec 18 14:41 export-with-emails.zip
    -rw-rw-r-- 1 bartek bartek  20M Dec 18 14:37 your-slack-team-export.zip

> clone and start

    git clone https://github.com/mattermost/mattermost-docker.git
    cd mattermost-docker
    mkdir -p ./volumes/app/mattermost/{data,logs,config,plugins}
    sudo chown -R 2000:2000 ./volumes/app/mattermost/
    vim docker-compose.yml
    docker-compose up -d

> create first user and configure at https://klub.brak.dev

    Site URL: https://klub.brak.dev  # https://klub.brak.dev/admin_console/general/configuration
    Max Users Per Team: 500  # https://klub.brak.dev/admin_console/site_config/users_and_teams
    Enable account creation with email: false  # Enable account creation with email:
    https://klub.brak.dev/admin_console/notifications/notifications_email

> continue export

    docker cp export-with-attachments.zip mattermost-docker_app_1:/

    docker-compose exec app ash
    mattermost import slack aa /export-with-attachments.zip


        Mattermost Slack Import Log

        Users created:
        ===============

        Slack user with email ?@slack-corp.com and password - has been imported.
        Slack user with email ?@brak.dev and password - has been imported.
        Slack user with email ?@botmail.bid and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        User github does not have an email address in the Slack export. Used github@example.com as a placeholder. The user should update their email address once logged in to the system.
        Slack user with email ?@example.com and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        Slack user with email ?@o2.pl and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        Slack user with email ?@gmail.com and password - has been imported.
        The Integration/Slack Bot user with email slackimportuser_ci7zoyuyf3nibq1zftd9nszasw@localhost and password - has been imported.
        ...

        Channels added:
        =================

        __main__
        random
        helpme
        tools
        books
        philosophy
        security
        mongohate
        jobs
        vent
        debugging
        test
        heheszki
        math
        rozrywka
        sneek
        dupa_channel
        trivia
        algo
        nsfw
        party
        like
        code
        imlame
        beginners
        imfame
        internet
        data
        law
        arch
        siseprojects
        sideprojects
        talks
        frontend
        aanandandrooioid
        polityko
        targ
        meta
        nocne_rozkminy
        instagram
        docker
        lang
        trip
        toptal-rekrutacja
        news
        hajsy
        warsztaty_2019_02_23
        integracja
        system
        codalej
        oditorium
        diy
        brakslak2
        b2b
        surprise
        word-of-the-day
        słowo-dnia
        chwalesie
        market
        php
        ncbi
        db
        toptal

        Notes:
        =======

        - Some messages may not have been imported because they were not supported by this importer.
        - Slack bot messages are currently not supported.
        - Additional errors may be found in the server logs.


        Finished Slack Import.

    rm /export-with-attachments.zip

> delete original messages

    \http 'https://slack.com/api/channels.list?token=xoxp-16083099889-16083793111-???&pretty=1' | jq -r '.channels[].name' | xargs -n 1 slack-cleaner --token=$token --message --user "*" --rate 0.1 --perform --channel

