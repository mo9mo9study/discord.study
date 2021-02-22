const {google} = require('googleapis');
//-----------------------------------------------------------------------
const keyfile='./api-project-xxxxxxxxxxxx-7c5ac86d4f1b.json';
const calendarId='ju67qphu1bk7dp5hdnjg63nlns@group.calendar.google.com';
console.log(keyfile)
//-----------------------------------------------------------------------
const event = {
  'summary': 'Test',
  'location': 'Tokyo',
  'description': '',
  'start': {
    'dateTime': '2020-08-13T10:00:00',
    'timeZone': 'Asia/Tokyo',
  },
  'end': {
    'dateTime': '2020-08-13T11:00:00',
    'timeZone': 'Asia/Tokyo',
  },
  'attendees': [],
  'colorId': 1,
  'reminders': {
    'useDefault': false,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
};
//----------------------------------------------------------------------- 
process.env.GOOGLE_APPLICATION_CREDENTIALS = keyfile
const key = require(keyfile);
const scope = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events'];
const jwt = new google.auth.JWT(key.client_email, null, key.private_key, scope)
const calendar = google.calendar("v3");

jwt.authorize((err, response) => {
      calendar.events.insert({
        auth: jwt,
        calendarId: calendarId,
        resource: event,
      }, (err, event) => {
        if (err) {
          console.log('ERROE' + err);
          return;
        }
        console.log('insertCalendar OK');
      });
})
