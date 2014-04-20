xquery version "1.0-ml";

(:~
: setup.xqy
: Sets up necessary infrastructure for the application to be built
:
: Note: You MUST run this against the App-Services Content Source in order to correctly 
: set up the ReST Application Server
:
: <ul>
: <li> Database and Forest</li>
: <li> Range Indexes</li>
: <li> ReST Application server?</li>
: </ul>
:
: @version 0.1
:)

import module namespace admin = "http://marklogic.com/xdmp/admin" at "/MarkLogic/admin.xqy";
import module namespace info = "http://marklogic.com/appservices/infostudio"  at "/MarkLogic/appservices/infostudio/info.xqy";
import module namespace rest-model="http://marklogic.com/appservices/infostudio/models/restful" at "/infostudio/models/rest-model.xqy";

declare variable $FOREST_MOUNTPOINT as xs:string := "E:\"; 
declare variable $CONFIG := admin:get-configuration();
declare variable $DATABASE-NAME as xs:string := "enron";
declare variable $APPSERVER-NAME as xs:string := "enron-http-rest";
declare variable $REST-SERVER-PORT := 8003;

(: 1. create db 
info:database-create($DATABASE-NAME, 1, "Default", $FOREST_MOUNTPOINT, "Security", "Schemas", "Triggers") :)

(: 2. configure range indexes :)
declare function local:create-range-indexes() { 
    
    let $rangespec := 
    (
        admin:database-range-element-index("string", (), "Subject", "http://marklogic.com/collation/codepoint", fn:false() ),
        admin:database-range-element-index("string", (), "From", "http://marklogic.com/collation/codepoint", fn:false() ),
        admin:database-range-element-index("string", (), "To", "http://marklogic.com/collation/codepoint", fn:false() ),
        admin:database-range-element-index("dateTime", (), "DateTime", (), fn:false() )
    )
    let $CONFIG := admin:database-add-range-element-index($CONFIG, xdmp:database($DATABASE-NAME), $rangespec)
    return
    admin:save-configuration($CONFIG)
};

(: 3. create ReST server 
rest-model:create-restful-server("enronY", "test-rest", 8005, "Default") :)

(: 4. set authentication to basic so the python script can connect :)
declare function local:configure-rest-server() {
    let $config := admin:get-configuration()
    let $groupid := admin:group-get-id($config, "Default")
    let $config := admin:appserver-set-authentication($config, 
         admin:appserver-get-id($config, $groupid, $APPSERVER-NAME), "basic")
    return
    admin:save-configuration($config)    
};


(: Module Main Section :)
(
    info:database-create($DATABASE-NAME, 1, "Default", $FOREST_MOUNTPOINT, "Security", "Schemas", "Triggers"),
    local:create-range-indexes(),
    rest-model:create-restful-server($DATABASE-NAME, $APPSERVER-NAME, $REST-SERVER-PORT, "Default"),
    local:configure-rest-server()
)