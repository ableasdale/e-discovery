xquery version "1.0-ml";

(: Single example for document-filter :)

let $doc :=  xdmp:document-get("C:\Users\Public\Music\Sample Music\Kalimba.mp3",
       <options xmlns="xdmp:document-get"
                xmlns:http="xdmp:http">
           <format>binary</format>
       </options>)
return
xdmp:document-filter($doc)

