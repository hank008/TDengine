###################################################################
#           Copyright (c) 2016 by TAOS Technologies, Inc.
#                     All rights reserved.
#
#  This file is proprietary and confidential to TAOS Technologies.
#  No part of this file may be reproduced, stored, transmitted,
#  disclosed or used in any form or by any means other than as
#  expressly provided by the written permission from Jianhui Tao
#
###################################################################

# -*- coding: utf-8 -*-

from frame import etool
from frame.etool import *
from frame.log import *
from frame.cases import *
from frame.sql import *
from frame.caseBase import *
from frame.common import *

class TDTestCase(TBase):
    def init(self, conn, logSql, replicaVar=1):
        self.replicaVar = int(replicaVar)
        tdLog.debug(f"start to excute {__file__}")
        tdSql.init(conn.cursor(), True)

    def insert_data(self):
        tdLog.info("insert interval test data.")
        # taosBenchmark run
        json = etool.curFile(__file__, "interval.json")
        etool.benchMark(json = json)

    def create_streams(self):
        tdSql.execute("use test;")
        streams = [
            "create stream stream1 fill_history 1 into sta as select _wstart, _wend, _wduration, count(*) from test.st where ts < '2020-10-01 00:07:19' interval(1m, auto);",
            "create stream stream2 fill_history 1 into stb as select _wstart, _wend, _wduration, count(*) from test.st where ts = '2020-11-01 23:45:00' interval(1h, auto) sliding(27m);",
            "create stream stream3 fill_history 1 into stc as select _wstart, _wend, _wduration, count(*) from test.st where ts in ('2020-11-12 23:32:00') interval(1n, auto) sliding(13d);",
            "create stream stream4 fill_history 1 into std as select _wstart, _wend, _wduration, count(*) from test.st where ts in ('2020-10-09 01:23:00', '2020-11-09 01:23:00', '2020-12-09 01:23:00') interval(1s, auto);",
            "create stream stream5 fill_history 1 into ste as select _wstart, _wend, _wduration, count(*) from test.st where ts > '2020-12-09 01:23:00' interval(1d, auto) sliding(17h);",
            "create stream stream6 fill_history 1 into stf as select _wstart, _wend, _wduration, count(*) from test.st where ts >= '2020-10-09 01:23:00' interval(1n, auto);",
            "create stream stream7 fill_history 1 into stg as select _wstart, _wend, _wduration, count(*) from test.st where ts >= '2020-11-09 01:23:00' interval(1n, auto) sliding(13d);",
        ]
        for sql in streams:
            tdSql.execute(sql)
        for i in range(50):
            rows = tdSql.query("select * from information_schema.ins_stream_tasks where history_task_status is not null;")
            if rows == 0:
                break;
            tdLog.info(f"i={i} wait for history data calculation finish ...")
            time.sleep(1)

    def query_test(self):
        # read sql from .sql file and execute
        tdLog.info("test normal query.")
        self.sqlFile = etool.curFile(__file__, f"in/interval.in")
        self.ansFile = etool.curFile(__file__, f"ans/interval.csv")

        tdCom.compare_testcase_result(self.sqlFile, self.ansFile, "interval")

    def run(self):
        self.insert_data()
        self.create_streams()
        self.query_test()

    def stop(self):
        tdSql.execute("drop stream stream1;")
        tdSql.execute("drop stream stream2;")
        tdSql.execute("drop stream stream3;")
        tdSql.execute("drop stream stream4;")
        tdSql.execute("drop stream stream5;")
        tdSql.execute("drop stream stream6;")
        tdSql.execute("drop stream stream7;")
        tdLog.success(f"{__file__} successfully executed")


tdCases.addLinux(__file__, TDTestCase())
tdCases.addWindows(__file__, TDTestCase())
