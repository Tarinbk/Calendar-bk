from django.shortcuts import render
import calendar
from datetime import date

def index(request):
    today = date.today()
    
    # 1. รับค่าปีจาก Filter (ค่าเริ่มต้นคือปีปัจจุบัน)
    year_str = request.GET.get('year', str(today.year))
    try:
        year = int(year_str)
    except ValueError:
        year = today.year

    # 2. ข้อมูลวันหยุดคงที่ (Fixed Solar Holidays)
    fixed_holidays = {
        (1, 1): "วันขึ้นปีใหม่",
        (4, 6): "วันจักรี",
        (4, 13): "วันสงกรานต์",
        (4, 14): "วันครอบครัว",
        (4, 15): "วันสงกรานต์",
        (5, 1): "วันแรงงาน",
        (5, 4): "วันฉัตรมงคล",
        (6, 3): "วันเฉลิมฯ พระราชินี",
        (7, 28): "วันเฉลิมฯ ร.10",
        (8, 12): "วันแม่แห่งชาติ",
        (10, 13): "วันนวมินทรมหาราช",
        (10, 23): "วันปิยมหาราช",
        (12, 5): "วันพ่อแห่งชาติ",
        (12, 10): "วันรัฐธรรมนูญ",
        (12, 31): "วันสิ้นปี",
    }
    
    # ข้อมูลวันสำคัญทางจันทรคติ (จำลองสำหรับปี 2026 - วันจริงเปลี่ยนทุกปี)
    lunar_holidays_2026 = {
        (3, 3): "วันมาฆบูชา",
        (5, 31): "วันวิสาขบูชา",
        (7, 29): "วันอาสาฬหบูชา",
        (7, 30): "วันเข้าพรรษา",
        (10, 26): "วันออกพรรษา",
    }
    
    months_data = []
    for month_num in range(1, 13):
        month_name = calendar.month_name[month_num]
        weeks = calendar.monthcalendar(year, month_num)
        
        weeks_with_holidays = []
        for week in weeks:
            days_info = []
            for d in week:
                if d == 0:
                    days_info.append({'day': 0, 'holiday': None, 'is_wan_phra': False})
                else:
                    holiday_text = fixed_holidays.get((month_num, d))
                    is_wan_phra = False
                    
                    # ถ้าเป็นปี 2026 ให้ใส่วันจันทรคติด้วย
                    if year == 2026 and not holiday_text:
                        holiday_text = lunar_holidays_2026.get((month_num, d))
                        
                    # จำลอง "วันพระ" คร่าวๆ (เช่น วันที่ 8, 15, 23 ของทุกเดือน เพื่อความสวยงาม)
                    if not holiday_text and d in [8, 15, 23, 29]:
                        holiday_text = "วันพระ"
                        is_wan_phra = True
                        
                    days_info.append({
                        'day': d,
                        'holiday': holiday_text,
                        'is_wan_phra': is_wan_phra
                    })
            weeks_with_holidays.append(days_info)
            
        months_data.append({
            'num': month_num,
            'name': month_name,
            'weeks': weeks_with_holidays
        })
        
    # 3. เตรียมรายการปีสำหรับ Dropdown (ย้อนหลัง 50 ปี ถึงอนาคต 50 ปี)
    years_list = range(today.year - 50, today.year + 51)
        
    context = {
        'year': year,
        'months_data': months_data,
        'today': today,
        'years_list': years_list,
    }
    return render(request, 'app_calendar/index.html', context)
