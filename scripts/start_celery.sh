if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

CELERY_CONCURRENCY=${CELERY_CONCURRENCY:-4}

celery -A core worker -B -E -n worker --loglevel=INFO --concurrency=$CELERY_CONCURRENCY
