import boto3
import delorean
import pytz
import requests
from dateutil import parser
from delorean import Delorean
from delorean import stops

# TODO load coordinates from text files
cities = [
    {
        "name": "munich",
        "coordinates": ([48.131726, 11.549377],
                        [48.106973, 11.558304],
                        [48.135621, 11.576328],
                        [48.160818, 11.549549],
                        [48.170665, 11.625423],
                        [48.139745, 11.623192],
                        [48.112016, 11.598473])
    },
    {
        "name": "passau",
        "coordinates": ([48.565816, 13.413019],
                        [48.573654, 13.455248])

    },
    {
        "name": "regensburg",
        "coordinates": ([49.015412, 12.063074],
                        [49.000380, 12.100239],
                        [49.031622, 12.106504])
    }
]

dynamodb = boto3.resource(
    'dynamodb',
    region_name='eu-central-1'
)

table = dynamodb.Table('events')

with table.batch_writer(overwrite_by_pkeys=['id', 'startTime']) as batch:
    for stop in stops(freq=delorean.DAILY, count=7):
        since = int(Delorean(stop.start_of_day).epoch)
        until = int(Delorean(stop.end_of_day).epoch)

        for city in cities:
            for lat, lng in city["coordinates"]:

                payload = {"lat": lat, "lng": lng, "distance": "2000",
                           "sort": "time", "since": since, "until": until}

                print(str(payload))

                r = requests.get("http://localhost:3000/events", params=payload)
                data = r.json()

                if "events" in data:
                    events = data["events"]

                    print("Found " + str(len(events)) + " events")

                    for event in events:

                        id = event["id"]
                        name = event["name"]
                        description = event["description"]

                        startTime = parser.parse(event["startTime"]).astimezone(pytz.utc).isoformat()

                        endTime = event["endTime"]
                        if endTime:
                            endTime = parser.parse(event["endTime"]).astimezone(pytz.utc).isoformat()

                        imageUrl = event["profilePicture"]
                        category = event["category"]

                        zip = " "
                        street = " "

                        location = event["venue"]["location"]

                        if "street" in location:
                            street = location["street"]

                        if "zip" in location:
                            zip = location["zip"]

                        venue = {
                            'name': event["venue"]["name"],
                            'zip': zip,
                            'street': street
                        }

                        batch.put_item(
                            Item={
                                'id': id,
                                'city': city["name"],
                                'description': description,
                                'imageUrl': imageUrl,
                                'name': name,
                                'startTime': startTime,
                                'endTime': endTime,
                                'category': str(category),
                                'venue': venue
                            })
