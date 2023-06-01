from datetime import date


def jsonify_data_record(record):
    return {
        "id": record.id,
        "text": record.text,
        "headings": record.headings,
        "file_type": record.file_type,
        "date": date.strftime(record.date, "%Y-%m-%d"),
        "user_id": record.user_id
    }
