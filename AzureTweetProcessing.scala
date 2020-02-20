def requestFormatter(givenTweet:String,i:Long):String={
  s"""{
    "documents":[
        {
        "language":"en",
        "id":${i},
        "text":"${givenTweet}"
        }
    ]
  }"""
}

def sendPostRequest(textAnalyticsUrl:String,subscriptionKey:String,requestBody:String):String={
  import scalaj.http.Http
  Thread.sleep(3000)
  val result = Http(textAnalyticsUrl).postData(requestBody)
  .header("Content-Type", "application/json")
  .header("Ocp-Apim-Subscription-Key", subscriptionKey).asString
  result.body
}

def removeHttpLines(textLine:String):Boolean={
  import scala.util.matching.Regex
  val pattern = "^http".r
  pattern.findFirstIn(textLine) match {
    case Some(x)=>false
    case _ => true
  }
}

case class textInformation(name:String, score:Double)
case class ResponseBody(id:String, detectedLanguages: List[textInformation])
case class AzureTextAnalyticsResponse(documents: List[ResponseBody], errors: List[String])

object ResponseJsonUtility extends java.io.Serializable {
 import spray.json._
 import DefaultJsonProtocol._
  
object MyJsonProtocol extends DefaultJsonProtocol {
 implicit val textInformationFormat = jsonFormat(textInformation, "name", "score")
 implicit val responseBodyFormat = jsonFormat(ResponseBody,"id","detectedLanguages") //this represents the inner document object of the Json
 implicit val responseFormat = jsonFormat(AzureTextAnalyticsResponse,"documents","errors") //this represents the outer key-value pairs of the Json
 }
//and lastly, a function to parse the Json (string) needs to be written which after parsing the Json string returns data in the form of case class object.
import MyJsonProtocol._
 import spray.json._
 
 def parser(givenJson:String):AzureTextAnalyticsResponse = {
 givenJson.parseJson.convertTo[AzureTextAnalyticsResponse]
 }
}

val url = "https://eastus.api.cognitive.microsoft.com/text/analytics/v3.0-preview.1/sentiment"
val subscriptionKey = "9c4d52dc3cce4af3b897ec336a02b6ff"

val tweetsSentimentsRdd = sc.textFile("/FileStore/tables/JennisonTweets2.txt").filter(removeHttpLines).zipWithIndex.map({ case (element, index) => requestFormatter(element,index)}).map(y=>sendPostRequest(url,subscriptionKey,y))

val tweetsSentimentList = tweetsSentimentsRdd.collect()
