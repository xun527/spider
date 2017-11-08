cd `dirname $0` || exit 1
scrapy crawl jd >> ./run.log 2>&1