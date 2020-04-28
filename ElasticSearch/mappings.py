users = {
  "mappings": {
    "properties": {
      "registration_date": {
        "type": "date" 
      },
      "first_name":{
      	"type":"text"
      },
      "last_name":{
      	"type":"text"
      },
      "username":{
      	"type":"text"
      },
      "email":{
      	"type":"text"
      },
      "password":{
      	"type":"text"
      }
    }
  }
}

posts = {
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
      },
      "content":{
      	"type":"text"
      },
      "post_id":{
      	"type":"integer"
      },
      "username":{
      	"type":"text"
      },
      "email":{
      	"type":"text"
      },
      "user_id":{
      	"type":"integer"
      }
    }
  }
}

comments = {
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis" 
      },
      "sender_username":{
      	"type":"text"
      },
      "post_id":{
      	"type":"integer"
      },
      "comment_content":{
      	"type":"text"
      },
      "sender_email":{
      	"type":"text"
      },
      "sender_id":{
      	"type":"integer"
      },
      "comment_id":{
        "type":"integer"
       }   
    }
  }
}