import sys
from util.log import *
from util.cases import *
from util.sql import *
from util.dnodes import tdDnodes
from math import inf

class TDTestCase:
    def caseDescription(self):
        '''
        case1<shenglian zhou>: [TD-11204]Difference improvement that can ignore negative
        '''
        return

    def init(self, conn, logSql, replicaVer=1):
        tdLog.debug("start to execute %s" % __file__)
        tdSql.init(conn.cursor(), False)
        self._conn = conn

    def restartTaosd(self, index=1, dbname="db"):
        tdDnodes.stop(index)
        tdDnodes.startWithoutSleep(index)
        tdSql.execute(f"use scd")

    def run(self):
        print("running {}".format(__file__))
        tdSql.execute("drop database if exists scd")
        tdSql.execute("create database if not exists scd compact_interval 0")
        tdSql.execute('use scd')
        tdSql.execute('create table stb1 (ts timestamp, c1 bool, c2 tinyint, c3 smallint, c4 int, c5 bigint, c6 float, c7 double, c8 binary(10), c9 nchar(10), c10 tinyint unsigned, c11 smallint unsigned, c12 int unsigned, c13 bigint unsigned) TAGS(t1 int, t2 binary(10), t3 double);')

        tdSql.execute("create table tb1 using stb1 tags(1,'1',1.0);")

        tdSql.execute("create table tb2 using stb1 tags(2,'2',2.0);")

        tdSql.execute("create table tb3 using stb1 tags(3,'3',3.0);")

        tdSql.execute('create database scd2 stt_trigger 3 compact_interval 1;')

        tdSql.execute('create database scd4 stt_trigger 13 compact_interval 12h compact_time_range -60,-10 compact_time_offset 23h;')

        tdSql.query('show create database scd;')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, 'scd')
        tdSql.checkData(0, 1, "CREATE DATABASE `scd` BUFFER 256 CACHESIZE 1 CACHEMODEL 'none' COMP 2 DURATION 10d WAL_FSYNC_PERIOD 3000 MAXROWS 4096 MINROWS 100 STT_TRIGGER 2 KEEP 3650d,3650d,3650d PAGES 256 PAGESIZE 4 PRECISION 'ms' REPLICA 1 WAL_LEVEL 1 VGROUPS 2 SINGLE_STABLE 0 TABLE_PREFIX 0 TABLE_SUFFIX 0 TSDB_PAGESIZE 4 WAL_RETENTION_PERIOD 3600 WAL_RETENTION_SIZE 0 KEEP_TIME_OFFSET 0h ENCRYPT_ALGORITHM 'none' S3_CHUNKPAGES 131072 S3_KEEPLOCAL 525600m S3_COMPACT 1 COMPACT_INTERVAL 0d COMPACT_TIME_RANGE 0d,0d COMPACT_TIME_OFFSET 0h")

        tdSql.query('show create database scd2;')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, 'scd2')
        tdSql.checkData(0, 1, "CREATE DATABASE `scd2` BUFFER 256 CACHESIZE 1 CACHEMODEL 'none' COMP 2 DURATION 10d WAL_FSYNC_PERIOD 3000 MAXROWS 4096 MINROWS 100 STT_TRIGGER 3 KEEP 3650d,3650d,3650d PAGES 256 PAGESIZE 4 PRECISION 'ms' REPLICA 1 WAL_LEVEL 1 VGROUPS 2 SINGLE_STABLE 0 TABLE_PREFIX 0 TABLE_SUFFIX 0 TSDB_PAGESIZE 4 WAL_RETENTION_PERIOD 3600 WAL_RETENTION_SIZE 0 KEEP_TIME_OFFSET 0h ENCRYPT_ALGORITHM 'none' S3_CHUNKPAGES 131072 S3_KEEPLOCAL 525600m S3_COMPACT 1 COMPACT_INTERVAL 1d COMPACT_TIME_RANGE -3650d,-10d COMPACT_TIME_OFFSET 0h")

        tdSql.query('show create database scd4')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, 'scd4')
        tdSql.checkData(0, 1, "CREATE DATABASE `scd4` BUFFER 256 CACHESIZE 1 CACHEMODEL 'none' COMP 2 DURATION 10d WAL_FSYNC_PERIOD 3000 MAXROWS 4096 MINROWS 100 STT_TRIGGER 13 KEEP 3650d,3650d,3650d PAGES 256 PAGESIZE 4 PRECISION 'ms' REPLICA 1 WAL_LEVEL 1 VGROUPS 2 SINGLE_STABLE 0 TABLE_PREFIX 0 TABLE_SUFFIX 0 TSDB_PAGESIZE 4 WAL_RETENTION_PERIOD 3600 WAL_RETENTION_SIZE 0 KEEP_TIME_OFFSET 0h ENCRYPT_ALGORITHM 'none' S3_CHUNKPAGES 131072 S3_KEEPLOCAL 525600m S3_COMPACT 1 COMPACT_INTERVAL 12h COMPACT_TIME_RANGE -60d,-10d COMPACT_TIME_OFFSET 23h")


        self.restartTaosd(1, dbname='scd')

        tdSql.query('show create database scd;')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, 'scd')
        tdSql.checkData(0, 1, "CREATE DATABASE `scd` BUFFER 256 CACHESIZE 1 CACHEMODEL 'none' COMP 2 DURATION 10d WAL_FSYNC_PERIOD 3000 MAXROWS 4096 MINROWS 100 STT_TRIGGER 2 KEEP 3650d,3650d,3650d PAGES 256 PAGESIZE 4 PRECISION 'ms' REPLICA 1 WAL_LEVEL 1 VGROUPS 2 SINGLE_STABLE 0 TABLE_PREFIX 0 TABLE_SUFFIX 0 TSDB_PAGESIZE 4 WAL_RETENTION_PERIOD 3600 WAL_RETENTION_SIZE 0 KEEP_TIME_OFFSET 0h ENCRYPT_ALGORITHM 'none' S3_CHUNKPAGES 131072 S3_KEEPLOCAL 525600m S3_COMPACT 1 COMPACT_INTERVAL 0d COMPACT_TIME_RANGE 0d,0d COMPACT_TIME_OFFSET 0h")

        tdSql.query('show create database scd2;')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, 'scd2')
        tdSql.checkData(0, 1, "CREATE DATABASE `scd2` BUFFER 256 CACHESIZE 1 CACHEMODEL 'none' COMP 2 DURATION 10d WAL_FSYNC_PERIOD 3000 MAXROWS 4096 MINROWS 100 STT_TRIGGER 3 KEEP 3650d,3650d,3650d PAGES 256 PAGESIZE 4 PRECISION 'ms' REPLICA 1 WAL_LEVEL 1 VGROUPS 2 SINGLE_STABLE 0 TABLE_PREFIX 0 TABLE_SUFFIX 0 TSDB_PAGESIZE 4 WAL_RETENTION_PERIOD 3600 WAL_RETENTION_SIZE 0 KEEP_TIME_OFFSET 0h ENCRYPT_ALGORITHM 'none' S3_CHUNKPAGES 131072 S3_KEEPLOCAL 525600m S3_COMPACT 1 COMPACT_INTERVAL 1d COMPACT_TIME_RANGE -3650d,-10d COMPACT_TIME_OFFSET 0h")
        tdSql.query('show create database scd4')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, 'scd4')
        tdSql.checkData(0, 1, "CREATE DATABASE `scd4` BUFFER 256 CACHESIZE 1 CACHEMODEL 'none' COMP 2 DURATION 10d WAL_FSYNC_PERIOD 3000 MAXROWS 4096 MINROWS 100 STT_TRIGGER 13 KEEP 3650d,3650d,3650d PAGES 256 PAGESIZE 4 PRECISION 'ms' REPLICA 1 WAL_LEVEL 1 VGROUPS 2 SINGLE_STABLE 0 TABLE_PREFIX 0 TABLE_SUFFIX 0 TSDB_PAGESIZE 4 WAL_RETENTION_PERIOD 3600 WAL_RETENTION_SIZE 0 KEEP_TIME_OFFSET 0h ENCRYPT_ALGORITHM 'none' S3_CHUNKPAGES 131072 S3_KEEPLOCAL 525600m S3_COMPACT 1 COMPACT_INTERVAL 12h COMPACT_TIME_RANGE -60d,-10d COMPACT_TIME_OFFSET 23h")


        tdSql.execute('drop database scd')
    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)

tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
