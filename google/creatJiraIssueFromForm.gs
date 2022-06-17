// This script takes the user inputs from the Google Form, and will create a JIRA issue when the form is submitted via the REST API
// Takes user input info, and passes it into an event parameter "e"
function createIssue(e){
// Assign variables to the form data submitted by the requestor from the spreasheet associated with the Google form.
// NOTE: Update the [n] to the cell value in your spreadsheet.
  var auth = [basic_64_conversion_of_username:APIKey_goes_here] //use https://www.base64encode.org/ to encode your username:Api Key
  
  var subject = e.values[1].toString();
  var email = e.values[2].toString();
  var priority = e.values[3].toString();
  var desc = e.values[4].toString();
  
  var deadlineArray = e.values[5].split("/"); //have to convert the dates into something jira will like. jira is very picky.
  if (deadlineArray[0].length < 2) {
    deadlineArray[0] = "0"+deadlineArray[0].toString()
  }
  if (deadlineArray[1].length < 2) {
    deadlineArray[1] = "0"+deadlineArray[0].toString()
  }
  var deadline = deadlineArray[2].toString() + "-" + deadlineArray[0].toString() + "-" + deadlineArray[1].toString()

  var description = "Description of request from "+email + ": "+desc;
  var url = "https://[ORG_URL_GOES_HERE].atlassian.net/rest/api/latest/issue";
  
// The POST data for the JIRA API call
  var data = {
    "fields": {
      "project":{
        "key": [PROJECT_KEY_GOES_HERE]
      },
      "summary": subject,
      "description": description,
      "priority": {"name": priority},
      "issuetype":{
        "name": "Task"
      },
      "duedate": deadline
    }
  };
  console.log(data)
//
// Turn all the post data into a JSON string to be send to the API
//
  var payload = JSON.stringify(data);
  var headers = {
    "content-type": "application/json",
    "Accept": "application/json",
    "authorization": "Basic " + auth.toString()
  };
// A final few options to complete the JSON string
  var options = {
    "content-type": "application/json",
    "method": "POST",
    "headers": headers,
    "payload": payload
  };
//
// Make the HTTP call to the JIRA API
//
  var response = UrlFetchApp.fetch(url, options);
  Logger.log(response.getContentText());
//
// Parse the JSON response to use the Issue Key returned by the API in the email
//
  var dataAll = JSON.parse(response.getContentText());
  var issueKey = dataAll.key;
  Logger.log(dataAll);
  console.log(dataAll);
  
  // moving the task off of the backlog and onto the actual board now
  var data2 = {"issues": [issueKey.toString()]}
  var payload2 = JSON.stringify(data2);
  var headers2 = {
    "content-type": "application/json",
    "Accept": "application/json",
    "authorization": "Basic " + auth.toString()
  };
  
  // A final few options to complete the JSON string
  var options = {
    "content-type": "application/json",
    "method": "POST",
    "headers": headers2,
    "payload": payload2
  };

// Make the HTTP call to the JIRA API to move the issue off the backlog
  var url2 = "https://[ORG_URL_GOES_HERE].atlassian.net/rest/agile/1.0/board/[BOARD_ID_GOES_HERE]/issue";
  var response = UrlFetchApp.fetch(url2, options);
  Logger.log(response);

// Assign variables for the email reposnse
  var emailSubject = "Your request no. " + issueKey + " has been created";
  var emailBody = "Thank you for your ticket submission." + "\n\n" +
    "Your request has been created, your reference is " + issueKey + " which can be accessed via the following link to the JIRA system:" + "\n\n" +
      "https://[ORG_URL_GOES_HERE].atlassian.net/browse/"+ issueKey + "\n\n" +
       "We will be in touch soon to discuss your ticket submission.  "
//
// Send an email to the requestor
//
MailApp.sendEmail(email, emailSubject, emailBody)
 }
