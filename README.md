<h1>movies_api_graphQL</hq>

<p>A small Django project aiming to establish GrapQL API.</p>

<h4>How to use</h4>

1. Clone this repository
2. Move to main directory and type:
  <strong>docker-compose up</strong>
  this will create a Postgres database and web application inside separate containers. 
3. Move to the container with the web application and migrate the data. When you are in your container type:
  <strong>python manage.py migrate</strong>
4. For test purposes you would like to create a superuser for your application. The reason for this is that mutations have @login_required authentication. Type:
  <strong>python manage.py createsuperuser</strong>
  Fill out credentials accordingly to the prompts in your terminal.
5. Move to the graphql/ endpoint and start testing an API. 
