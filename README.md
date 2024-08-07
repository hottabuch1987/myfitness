
[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=My+Fitness)](https://git.io/typing-svg)

# start  dev
### docker-compose build
### docker-compose up
# myfitness

# start  prod

# docker-compose -f docker-compose.prod.yml build
# docker-compose -f docker-compose.prod.yml up


# help commands
# docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
# docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
# docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
# docker exec myfitness_nginx_1 ls /home/app/web/static/images/team
# docker rmi -f b87dc131e33f