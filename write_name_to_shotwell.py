#!/usr/bin/python

# query the shotwell database
import sqlite3
import sys
import logging
import datetime
import traceback


def write_name_to_shotwell(img_path, match, shotwell_db):
    success = False
    try:
        conn = sqlite3.connect(shotwell_db)
        cur = conn.cursor()
        cur.execute('SELECT id FROM PhotoTable WHERE filename = ?', (img_path,))
        # record[0] holds id in decimal
        record = cur.fetchone()
        if record is None:
            raise UnboundLocalError('Bild %s in shotwell nicht gefunden', img_path)

        # construct thumb representation to look like thumb000.000.000.000.11a9,
        # aka thumb followed by 16 "digits" in hex
        img_hex = hex(record[0]).split('x')[-1]
        zeroes = '0'*(16 - len(img_hex))
        thumb = zeroes.join(['thumb', img_hex])

        cur.execute('SELECT photo_id_list FROM TagTable WHERE name = ?', (match,))
        thumb_list = cur.fetchone()

        # no tag for match exist
        if thumb_list is None:
            sqlite_insert_query = """INSERT INTO TagTable (name, photo_id_list, time_created) VALUES (?, ?, ?);"""
            insert_tuple = (match, thumb+',', datetime.datetime.now())
            cur.execute(sqlite_insert_query, insert_tuple)
            conn.commit()
            success = True
            logging.WARNING('Record inserted successfully into SqliteDb_developers table', cur.rowcount)

        # tags for match exist but do not point to img_path
        # we need first row of thumblist, it holds the value
        elif -1 == thumb_list[0].find(thumb):
            upd = thumb_list[0] + thumb + ','
            sql_update_query = """UPDATE TagTable SET photo_id_list = ? WHERE name = ?"""
            data = (upd, match)
            cur.execute(sql_update_query, data)
            conn.commit()
            success = True
            logging.WARNING('Record for %s Updated successfully with file %s!', match, thumb)

        # tags for match exist and point to target img_path
        else:
            logging.INFO('Record for %s already points to file %s!', match, thumb)
            success = True
            pass

    except UnboundLocalError as e:
        logging.ERROR(e.message)
        pass

    except sqlite3.Error as error:
        logging.ERROR('Failed to read image id from sqlite table', error.args[0])
        logging.DEBUG('SQLite error: %s' % (' '.join(error.args)))
        logging.DEBUG('Exception class is: ', error.__class__)
        exc_type, exc_value, exc_tb = sys.exc_info()
        logging.DEBUG('Traceback: ', traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
        if conn:
            conn.close()
        return success