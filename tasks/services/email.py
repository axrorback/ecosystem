from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags


def send_task_email(user, task):
    if not user.email:
        return

    full_name = user.first_name or user.username or "Team member"

    subject = f"[Task Assigned] {task.title}"

    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Salom, {full_name} 👋</h2>

            <p>Sizga <strong>yangi task</strong> biriktirildi.</p>

            <table cellpadding="6" cellspacing="0" border="0">
                <tr>
                    <td><strong>Task nomi:</strong></td>
                    <td>{task.title}</td>
                </tr>
                <tr>
                    <td><strong>Department:</strong></td>
                    <td>{task.department.name}</td>
                </tr>
                <tr>
                    <td><strong>Status:</strong></td>
                    <td>{task.status}</td>
                </tr>
                <tr>
                    <td><strong>Priority:</strong></td>
                    <td>{task.priority}</td>
                </tr>
    """

    if task.deadline:
        html_message += f"""
                <tr>
                    <td><strong>Deadline:</strong></td>
                    <td>{task.deadline:%d.%m.%Y %H:%M}</td>
                </tr>
        """

    html_message += "</table>"

    if task.description:
        html_message += f"""
            <p><strong>Tavsif:</strong></p>
            <p>{task.description}</p>
        """

    html_message += """
            <p style="margin-top: 20px;">
                Iltimos, taskni belgilangan muddatda bajarishni unutmang.
                Agar savollar bo‘lsa, team lead bilan bog‘laning.
            </p>

            <hr>
            <p style="font-size: 12px; color: #666;">
                Ushbu xabar avtomatik tarzda yuborildi.
            </p>
        </body>
    </html>
    """

    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
