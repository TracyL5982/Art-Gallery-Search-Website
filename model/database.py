"""module: luxserver.py
    pset group 17
    Tracy(Xinran) Li, Sianna Xiao"""
import argparse
from sys import exit, stderr
from contextlib import closing
from pickle import load, dump
from os import name
import sys
from socket import SOL_SOCKET, SO_REUSEADDR
import socket
from sqlite3 import connect, OperationalError, DatabaseError
from model.item import Artwork

DATABASE_URL = 'file:lux.sqlite?mode=ro'
_HEAD_UNDERLINE = "-"

def get_objects_info(label, agent, classification, date):
    """A section with header "Summary",
containing a single-row table with the following column headers and content:
"Accession No.", containing the accession number of the object
"Date", containing the object's date
"Place", containing the object's place
"Department", containing the object's department
"""
    artworks = []
    try:
        with connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                stmt_str = """
                        WITH cls AS (
                            SELECT id,
                                IFNULL(GROUP_CONCAT(lower(name),','), "")
                                as classifications
                            FROM (
                                SELECT
                                objects.id, lower(classifiers.name) as name
                                FROM objects
                                LEFT OUTER JOIN objects_classifiers ON objects.id = objects_classifiers.obj_id
                                LEFT OUTER JOIN classifiers ON objects_classifiers.cls_id = classifiers.id
                                ORDER BY lower(classifiers.name) ASC
                            )
                            GROUP BY id
                        ),

                        artists AS(
                            SELECT id,
                                    IFNULL(GROUP_CONCAT(agent,','), "") as artistParts
                            FROM (
                                SELECT
                                objects.id, (agents.name || " (" || productions.part ||")") as agent
                                FROM objects
                                LEFT OUTER JOIN productions ON objects.id = productions.obj_id
                                LEFT OUTER JOIN agents ON productions.agt_id = agents.id
                                ORDER BY agents.name ASC, productions.part ASC
                            )
                            GROUP BY id
                        )

                        SELECT
                            objects.label,
                            IFNULL(objects.date, ""),
                            artistParts,
                            classifications,
                            objects.id
                        FROM objects
                        NATURAL JOIN artists
                        NATURAL JOIN cls
                """
                arguments = []
                if label is not None:
                    arguments.append(("objects.label", label))

                if classification is not None:
                    arguments.append(("classifications", classification))

                if agent is not None:
                    arguments.append(("artistParts", agent))

                if date is not None:
                    arguments.append(("objects.date", date))

                clause = ""
                if len(arguments) != 0:
                    clause += " WHERE "
                    for argument in arguments:
                        clause += f"{argument[0]} LIKE '%{argument[1]}%' "
                        clause += "AND "
                    clause = clause[:len(clause)-4]

                stmt_str += clause
                stmt_str += "\n"
                stmt_str += "ORDER BY objects.label ASC, objects.date ASC\n"
                stmt_str += "LIMIT 1000;"

                cursor.execute(stmt_str)

                row = cursor.fetchone()
                while row is not None:
                    artwork = Artwork(str(row[0]), str(row[1]),str(row[2]), str(row[3]), str(row[4]))
                    artworks.append(artwork)
                    row = cursor.fetchone()
                return artworks
    except OperationalError:
        print("We're sorry - the table could not found")
        sys.exit(1)
    except DatabaseError:
        print("Your database could not be found or is corrupted.")
        sys.exit(1)

def summary(s_id):
    """A section with header "Summary"
"""
    try:
        with connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                stmt_str = """
                SELECT
                    IFNULL(o.accession_no, "") AS "Accession No.",
                    IFNULL(o.date, "") AS "Date",
                    IFNULL(GROUP_CONCAT(p.label, '|'), "") AS "Place",
                    IFNULL(d.name, "") AS "Department"
                FROM
                    objects AS o
                LEFT OUTER JOIN
                    objects_places AS op ON o.id = op.obj_id
                LEFT OUTER JOIN
                    places AS p ON op.pl_id = p.id
                LEFT OUTER JOIN
                    objects_departments AS od ON o.id = od.obj_id
                LEFT OUTER JOIN
                    departments AS d ON od.dep_id = d.id
                WHERE
                    o.id = ?
                GROUP BY o.id
                """

                cursor.execute(stmt_str, [s_id])
                rows = cursor.fetchall()
                if len(rows) == 0:
                    return None

                summ = {
                    "accession_no": rows[0][0],
                    "date": rows[0][1],
                    "place": rows[0][2]

                }
                return summ
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit()

def label(l_id):
    """A section with header "Label" containing the object's label
    """
    try:
        with connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                stmt_str = """
                SELECT
                    IFNULL(o.label, "") AS "Label"
                FROM
                    objects o
                WHERE
                    o.id = ?
                """
                cursor.execute(stmt_str, [l_id])
                rows = cursor.fetchall()
                return rows[0][0]
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit()

def produced_by(p_id):
    """A section with header "Produced By",
    containing a table with details of all agents that produced this object.
    The table must have the following column headers and content:
    "Part", containing the part(s) of the production carried out by each agent
    "Name", containing the name of each agent
    "Nationalities", containing all nationalities of each agent, each on its own line
    "Timespan", containing the year of each agent's begin_date
    and the year of each agent's end_date,
    separated by an en dash character ('–', "\u2013")
    Some agents are still alive/active;
    in those cases the Timespan column must contain text such as "1967–"
    This list must be sorted in ascending order of agent name, then part, and finally by nationality
    """
    string = "Produced By\n"
    string += _HEAD_UNDERLINE * 20 + "\n"
    try:
        with connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                stmt_str = """
                WITH AgentDetails AS (
                    SELECT
                        IFNULL(p.part,"") AS "Part",
                        IFNULL(a.name,"") AS "Name",
                        IFNULL(GROUP_CONCAT(n.descriptor, CHAR(10)), "") AS "Nationalities",
                        CASE
                            WHEN a.end_date IS NULL THEN CAST(strftime('%Y', a.begin_date) AS VARCHAR(10)) || '–'
                            ELSE CAST(strftime('%Y', a.begin_date) AS VARCHAR(10)) || '–' || CAST(strftime('%Y', a.end_date) AS VARCHAR(10))
                        END AS "Timespan"
                    FROM
                        productions p
                    LEFT OUTER JOIN
                        agents a ON p.agt_id = a.id
                    LEFT OUTER JOIN
                        agents_nationalities an ON a.id = an.agt_id
                    LEFT OUTER JOIN
                        nationalities n ON an.nat_id = n.id
                    WHERE
                        p.obj_id = ?
                    GROUP BY
                        p.part, a.name, "Timespan"
                )
                SELECT
                    "Part",
                    "Name",
                    "Nationalities",
                    "Timespan"
                FROM
                    AgentDetails
                ORDER BY
                    "Name" ASC,
                    "Part" ASC,
                    "Nationalities" ASC
                """

                cursor.execute(stmt_str, [p_id])
                rows = cursor.fetchall()
                ret = []
                for row in rows:
                    ret.append({
                        "part": row[0],
                        "name": row[1],
                        "nationalities": row[2],
                        "timespan": row[3]
                    })
                return ret
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit()
    print()

def classified_as(c_id):
    """A section with header "Classified As", containing a list of
    all classifiers for the object, with one per line
This list must be sorted in ascending order of the classifier name
    """
    try:
        with connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                stmt_str = """
                SELECT
                    IFNULL(lower(c.name),"") AS "Classified As"
                FROM
                    objects_classifiers AS oc
                LEFT OUTER JOIN
                    classifiers AS c ON oc.cls_id = c.id
                WHERE
                    oc.obj_id = ?
                ORDER BY
                    lower(c.name) ASC
                """

                cursor.execute(stmt_str, [c_id])
                rows = cursor.fetchall()
                ret = []
                for row in rows:
                    ret.append(row[0])
                return ret
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit()
    print()

def information(i_id):
    """A section with header "Information", containing a table of all references to the object,
    with two columns: "Type" and "Content" (with the obvious values)
    """
    string = "Information\n"
    string += _HEAD_UNDERLINE * 20 + "\n"
    try:
        with connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                stmt_str = """
                SELECT
                    IFNULL(r.type,"") AS "Type",
                    IFNULL(r.content,"") AS "Content"
                FROM
                    "references" AS r
                WHERE
                    r.obj_id = ?
                """
                cursor.execute(stmt_str, [i_id])
                rows = cursor.fetchall()
                ret = []
                for row in rows:
                    ret.append({
                        "type": row[0],
                        "content": row[1]
                    })
                return ret
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit()

def get_objects_details(args):
    """
    displaying object details including summary, label, produced by, classified as, information
"""
    curr_id = str(args["id"])
    tables = []
    tables.append(summary(curr_id))
    tables.append(label(curr_id))
    tables.append(produced_by(curr_id))
    tables.append(classified_as(curr_id))
    tables.append(information(curr_id))
    return tables

def handle_client(sock):
    """
    communicate with the client: lux.py
    """

    in_flo = sock.makefile(mode='rb')
    args = load(in_flo)
    print(args)
    if args == '':
        print('The echo client crashed')
        return

    screen_width = load(in_flo)
    action = load(in_flo)

    if action == "get_info":
        objects = get_objects_info(args, screen_width)
    elif action == "details":
        objects = get_objects_details(args)
    else:
        print("action not supported", file = stderr)

    out_flo = sock.makefile(mode='wb')
    dump(objects, out_flo)
    out_flo.flush()

def parse_args():
    """parsing the arguments

    Returns:
        parsed arguments
    """
    parser = argparse.ArgumentParser(description='Server for the YUAG application',
                                     prog='luxserver.py', allow_abbrev=False,
                                     usage='%(prog) s' + '[-h] port')
    parser.add_argument('port', help='the port at which the server should listen')
    return parser.parse_args()

def main():
    """the main function
    """
    try:
        port = int(parse_args().port)

        server_sock = socket.socket()
        print('Opened server socket')
        if name != 'nt':
            server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            server_sock.bind(('', port))
        except socket.error:
            print("Unavailable port", file = stderr)
            exit(1)
        print('Bound server socket to port')
        server_sock.listen()
        print('Listening')

        while True:
            try:
                sock, client_addr = server_sock.accept()
                with sock:
                    print('Accepted connection')
                    print('Opened socket')
                    print('Server IP addr and port:',
                        sock.getsockname())
                    print('Client IP addr and port:', client_addr)
                    handle_client(sock)
            except socket.error as ex:
                print(ex, file=stderr)

    except socket.error as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
