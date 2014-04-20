xquery version "1.0-ml";

(: ROUGH teardown module :)

import module namespace rest-model="http://marklogic.com/appservices/infostudio/models/restful" at "/infostudio/models/rest-model.xqy";
import module namespace info = "http://marklogic.com/appservices/infostudio"  at "/MarkLogic/appservices/infostudio/info.xqy";

(info:database-delete("enronY"),
rest-model:delete-restful-server("test", "Default"))
