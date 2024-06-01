from core.database import database
from sqlalchemy.sql import select, and_
import pandas as pd
import datetime
from sqlalchemy.exc import IntegrityError
import logging


logger = logging.getLogger(__name__)
engine = database.engine
conn = engine.connect()


def insert_data_into_ohlcv_table(exchange, pair, interval, candle, pair_id):
    """Inserts exchange candle data into table"""
    logger.info('Adding candle with timestamp: ' + str(candle[0]))
    with database.lock:
        args = [exchange, pair, candle[0], candle[1], candle[2], candle[3], candle[4], candle[5], interval]
        ins = database.OHLCV.insert().values(Exchange=args[0], Pair=args[1], Timestamp=convert_timestamp_to_date(args[2]), Open=args[3], High=args[4], Low=args[5], Close=args[6], Volume=args[7], Interval=args[8], TimestampRaw=args[2], PairID=pair_id)
        conn.execute(ins)


def get_latest_candle(exchange, pair, interval):
    """Returns only latest candle if it exists, otherwise returns 0"""
    with database.lock:
        logger.info("Querying latest candle for " + exchange + " " + pair)
        s = select([database.OHLCV]).where(and_(database.OHLCV.c.Exchange == exchange, database.OHLCV.c.Pair == pair, database.OHLCV.c.Interval == interval)).order_by(database.OHLCV.c.TimestampRaw.desc()).limit(1)
        result = conn.execute(s)
        row = result.fetchone()
        result.close()
        return row

def get_all_candles(pair_id):
    with database.lock:
        logger.info("Retrieving all candles for pair " + str(pair_id))
        result = conn.execute("SELECT TimestampRaw, Open, High, Low, Close, Volume FROM OHLCV WHERE PairID = ?", (pair_id,))
        return [row for row in result]


def get_latest_N_candles_as_df(exchange, pair, interval, N):
    """Returns N latest candles for TA calculation purposes"""
    with database.lock:
        s = select([database.OHLCV]).where(and_(database.OHLCV.c.Exchange == exchange, database.OHLCV.c.Pair == pair, database.OHLCV.c.Interval == interval)).order_by(database.OHLCV.c.ID.desc()).limit(N)
        result = conn.execute(s)
        df = pd.DataFrame(result.fetchall())
        df.columns = result.keys()
        result.close()
        return df


def write_trade_pairs_to_db(exchange_id, base, quote, interval):
    """Returns the ID of the trade pair"""
    logger.info("Writing market data pair to DB")
    with database.lock:
        try:
            s = select([database.TradingPairs]).where(
                and_(database.TradingPairs.c.Exchange == exchange_id,
                     database.TradingPairs.c.BaseCurrency == base,
                     database.TradingPairs.c.QuoteCurrency == quote,
                     database.TradingPairs.c.Interval == interval))
            result = conn.execute(s).fetchone()
            if result is None:
                ins = database.TradingPairs.insert().values(Exchange=exchange_id, BaseCurrency=base, QuoteCurrency=quote, Interval=interval)
                conn.execute(ins)
                return conn.execute(s).cursor.lastrowid
            else:
                logger.info("Market data already available for pair, returning ID for lookups")
                return result[0]
        except IntegrityError:
            print("Pair already logged in DB")



def convert_timestamp_to_date(timestamp):
    value = datetime.datetime.fromtimestamp(float(str(timestamp)[:-3]))  #this might only work on bittrex candle timestamps
    return value.strftime('%Y-%m-%d %H:%M:%S')

