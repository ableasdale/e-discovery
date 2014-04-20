xquery version "1.0-ml";

(:~
: setup.xqy
: Sets up necessary infrastructure for the application to be built 
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

declare variable $FOREST_MOUNTPOINT as xs:string := "E:\"; 
declare variable $CONFIG := admin:get-configuration();
declare variable $DATABASE-NAME as xs:string := "enronY";

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

(: Module Main Section :)
(
    info:database-create($DATABASE-NAME, 1, "Default", $FOREST_MOUNTPOINT, "Security", "Schemas", "Triggers"),
    local:create-range-indexes()
)