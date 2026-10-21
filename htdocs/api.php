<?php
header("Content-Type: application/json");
header("Cache-Control: no-store, max-age=0");
$base = dirname(__DIR__) . "/JurnalMT5/data";
$rd = function($f) use ($base) { $p="$base/$f"; return file_exists($p)?json_decode(file_get_contents($p),true):([]); };
echo json_encode(["closed"=>$rd("closed.json"),"cash"=>$rd("cash_flow.json"),"report"=>$rd("ai_report.json"),"memory"=>$rd("ai_memory.json"),"open"=>$rd("open.json"),"account"=>$rd("account.json"),"meta"=>$rd("meta.json")], JSON_UNESCAPED_UNICODE);
