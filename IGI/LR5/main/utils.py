import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from django.utils import timezone
from .models import Driver, Client, Organization

def generate_user_types_pie_chart():
    """Генерирует круговую диаграмму распределения типов пользователей."""
    counts = {
        'Водители': Driver.objects.count(),
        'Клиенты (Физ. лица)': Client.objects.count(),
        'Организации (Клиенты)': Organization.objects.count(),
    }

    filtered_counts = {label: count for label, count in counts.items() if count > 0}

    if not filtered_counts:
        return None

    labels = list(filtered_counts.keys())
    sizes = list(filtered_counts.values())

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True,
           textprops={'fontsize': 10})
    ax.axis('equal')
    plt.title('Распределение типов пользователей', fontsize=14)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return f"data:image/png;base64,{image_base64}"

def calculate_age(birth_date):
    """Вспомогательная функция для расчета возраста."""
    if not birth_date:
        return None
    today = timezone.now().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def generate_ages_histogram():
    """Генерирует гистограмму распределения возрастов водителей и клиентов (физ. лиц)."""
    driver_ages = [calculate_age(driver.birth_date) for driver in Driver.objects.filter(birth_date__isnull=False)]
    client_ages = [calculate_age(client.birth_date) for client in Client.objects.filter(birth_date__isnull=False)]

    all_ages = [age for age in driver_ages + client_ages if age is not None and age >= 18]

    if not all_ages:
        return None

    fig, ax = plt.subplots(figsize=(10, 6))
    bins = range(15, 81, 5)
    ax.hist(all_ages, bins=bins, edgecolor='black', color='skyblue',
            rwidth=0.9)

    ax.set_xlabel('Возраст', fontsize=12)
    ax.set_ylabel('Количество пользователей', fontsize=12)
    plt.title('Распределение возрастов (Водители и Клиенты физ.лица)', fontsize=14)

    tick_labels = [f'{i}-{i + 4}' for i in bins[:-1]]
    ax.set_xticks([b + 2.5 for b in bins[:-1]])
    ax.set_xticklabels(tick_labels, rotation=45, ha="right")

    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return f"data:image/png;base64,{image_base64}"