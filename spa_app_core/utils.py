from spa_comments_app.models import Comment


def count_total_comments_and_replies(comment):
    total_replies = comment.replies.count()
    for reply in comment.replies.all():
        total_replies += count_total_comments_and_replies(reply)
    return total_replies + 1


def count_all_comments_and_replies(comments):
    total = 0
    for comment in comments:
        total += count_total_comments_and_replies(comment)
    return total
