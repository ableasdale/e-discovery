xquery version "1.0-ml";

(: Rough teardown module :)

import module namespace rest-model="http://marklogic.com/appservices/infostudio/models/restful" at "/infostudio/models/rest-model.xqy";
import module namespace info = "http://marklogic.com/appservices/infostudio"  at "/MarkLogic/appservices/infostudio/info.xqy";

(
(: 
These both require restarts - so need to be executed one-at-a-time!
rest-model:delete-restful-server("enron-http-rest", "Default"), 
rest-model:delete-restful-server("enron", "Default"),
:)
info:database-delete("enron"),
info:database-delete("enron-http-rest-modules"),
info:database-delete("enron-modules")
(: note you may need to delete the forest (enron-1) :)
)