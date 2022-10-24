#!/usr/bin/python

# query the shotwell database
import sqlite3
import sys
import logging
import datetime
import traceback


def write_name_to_shotwell(imagePath, match, shotwell_db):
    try:
        success = False
        conn = sqlite3.connect(shotwell_db)
        logging.info('writing %s for image %s to shotwells database', match, imagePath)
        cur = conn.cursor()
        cur.execute("SELECT id FROM PhotoTable WHERE filename = ?", (imagePath,))
        # record[0] holds id in decimal
        record = cur.fetchone()
        if record is None:
            raise UnboundLocalError("Bild %s in shotwell nicht gefunden", imagePath)

        # construct thumb representation to look like thumb000.000.000.000.11a9,
        # aka thumb followed by 16 "digits" in hex
        img_hex = hex(record[0]).split('x')[-1]
        zeroes = '0'*(16 - len(img_hex))
        thumb = zeroes.join(['thumb', img_hex])

        cur.execute("SELECT photo_id_list FROM TagTable WHERE name = ?", (match,))
        thumb_list = cur.fetchone()

        # no tag for match exist
        if thumb_list is None:
            sqlite_insert_query = """INSERT INTO TagTable (name, photo_id_list, time_created) VALUES (?, ?, ?);"""
            insert_tuple = (match, thumb+',', datetime.datetime.now())
            cur.execute(sqlite_insert_query, insert_tuple)
            conn.commit()
            success = True
            logging.warning("Record inserted successfully into SqliteDb_developers table", cur.rowcount)

        # tags for match exist but do not point to imagePath
        # we need first row of thumblist, it holds the value
        elif -1 == thumb_list[0].find(thumb):
            upd = thumb_list[0] + thumb + ','
            sql_update_query = """UPDATE TagTable SET photo_id_list = ? WHERE name = ?"""
            data = (upd, match)
            cur.execute(sql_update_query, data)
            conn.commit()
            success = True
            logging.warning("Record for %s Updated successfully with file %s !", match, thumb)

        # tags for match exist and point to target imagePath
        else:
            logging.info("Record for %s already points to file %s !", match, thumb)
            success = True
            # pass

    except UnboundLocalError as e:
        logging.error(e)
        pass

    except sqlite3.Error as error:
        logging.error("Failed to read image id from sqlite table", error.args[0])
        logging.debug("SQLite error: %s" % (' '.join(error.args)))
        logging.debug("Exception class is: ", error.__class__)
        exc_type, exc_value, exc_tb = sys.exc_info()
        logging.debug("Traceback: ", traceback.format_exception(exc_type, exc_value, exc_tb))

    finally:
        if conn:
            conn.close()

    return success