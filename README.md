# Cloud Function Deploy
gcloud functions deploy slackFilterKeyword --region=asia-northeast1 --trigger-http --env-vars-file env.yaml --runtime python310 --timeout=540 --entry-point=slack_events --allow-unauthenticated


gcloud config set project hoikutasu-develop;


gcloud functions deploy send-daily-notification-dev --env-vars-file dev.env.yaml --entry-point sendDailyNotification --runtime nodejs12 --trigger-http --allow-unauthenticated --region asia-northeast3


gcloud functions deploy filter-slack --runtime=python39 --region=asia-northeast1 --source=. --entry-point=send_to_slack --trigger-http --env-vars-file env.yaml --allow-unauthenticated


gcloud functions deploy search_keyword --gen2 --runtime=python39 --region=asia-northeast1 --source=. --entry-point=slack_message --trigger-http --allow-unauthenticated


gcloud functions deploy search_keyword --gen2 --region=asia-northeast1 --trigger-http --env-vars-file env.yaml --runtime python39 --timeout=540 --entry-point=slack_message --allow-unauthenticated