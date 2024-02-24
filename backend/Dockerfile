FROM python:3.10

WORKDIR /home/des/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Install nodejs
RUN apt-get update && apt-get install -y nodejs npm

COPY ./requirements.txt /home/des/backend/requirements.txt
RUN pip install -r requirements.txt

RUN npm install -g sass
# Copy and install Node.js dependencies
COPY ./package.json /home/des/backend/package.json
COPY ./package-lock.json /home/des/backend/package-lock.json

RUN npm install

RUN apt-get clean && rm -rf /var/lib/apt/lists/*