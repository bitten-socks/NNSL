from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# 1. 최종 질문 데이터
QUESTIONS = {
    "1": {"type": "Y/S", "question": "모임에서 첫눈에 반한 사람 발견 시?", "options": {"A": "적극적으로 말 걸기", "B": "신중히 기회 노리기"}},
    "2": {"type": "Y/S", "question": "썸 타는 중 더 매력적인 사람 등장 시?", "options": {"A": "새로운 사람 알아보기", "B": "현재 관계에 집중"}},
    "3": {"type": "O/G", "question": "깊은 대화를 나누는 분위기라면?", "options": {"A": "내 속마음 다 털어놓기", "B": "주로 들어주기"}},
    "4": {"type": "O/G", "question": "혹시 아직 미련 있어? 라는 질문을 받는다면?", "options": {"A": "솔직하게 인정하기", "B": "적당히 둘러대기"}},
    "5": {"type": "C/L", "question": "데이트 장소를 고르는 기준은?", "options": {"A": "분위기 좋은 감성 공간", "B": "효율적인 실용 맛집"}},
    "6": {"type": "C/L", "question": "친구 두 명이 크게 싸웠을 때?", "options": {"A": "적극적으로 중재하기", "B": "둘이 해결하게 두기"}}
}


# 2. 최종 캐릭터별 결과 데이터
RESULTS = {
    "male": {
        "YOC": [
            {"name": "영철", "catchphrase": "일단 GO! 풀악셀 직진남", "keywords": "#내사전에후진은없다 #인간불도저 #마!이게사랑이다 #의리파순정남", "compatibility": {"best": "옥순 (SOC)", "worst": "광수 (YGL)"}, "description": "당신은 목표가 생기면 뒤돌아보지 않고 돌진하는 '인간 불도저' 타입입니다. 복잡한 밀당이나 애매한 상황을 싫어하며, 솔직하고 거침없는 표현으로 자신의 마음을 보여주는 것을 선호합니다. 한번 마음을 주면 한 사람만 바라보는 의리파 순정남의 면모도 가지고 있어, 당신의 뜨거운 마음에 한번 빠지면 헤어나오기 어렵습니다."},
            {"name": "영호", "catchphrase": "분위기 메이커! 유쾌한 소셜 MC", "keywords": "#내가바로인간비타민 #분위기띄우기장인 #말이좀많을뿐 #유머감각탑재", "compatibility": {"best": "영자 (YOC)", "worst": "현숙 (SGL)"}, "description": "당신은 어떤 어색한 자리도 순식간에 화기애애하게 만드는 '인간 비타민'입니다. 뛰어난 화술과 유머 감각으로 대화를 주도하는 타고난 MC이며, 주변 사람들을 챙기는 데 익숙합니다. 활발하고 적극적인 에너지로 그룹의 중심이 되지만, 때로는 너무 많은 말 때문에 의도치 않은 말실수를 하기도 하는 귀여운 허당미를 가지고 있습니다."}
        ],
        "YGL": [{"name": "광수", "catchphrase": "예측불가! 고뇌하는 브레인", "keywords": "#알고보면천재 #내머릿속은아무도몰라 #고독한천재 #감정롤러코스터", "compatibility": {"best": "현숙 (SGL)", "worst": "영철 (YOC)"}, "description": "당신은 평범함을 거부하는, 자기만의 세계가 뚜렷한 '고독한 천재' 타입입니다. 명석한 두뇌와 논리를 가졌지만, 때로는 감정의 롤러코스터를 타며 예측불가한 행동으로 주변을 놀라게 합니다. 겉으로는 속을 알 수 없는 신비주의자처럼 보이지만, 한번 마음을 열면 누구보다 순수하고 깊은 관계를 맺고자 하는 열망을 가지고 있습니다."}],
        "SOC": [{"name": "상철", "catchphrase": "삶의 밸런스를 아는 유쾌한 안정감", "keywords": "#밸런스의수호자 #만인의친구 #결혼상대프리패스상 #알고보면인싸", "compatibility": {"best": "옥순 (SOC)", "worst": "순자 (YGL)"}, "description": "당신은 어느 한쪽에 치우치지 않는 '밸런스의 수호자'입니다. 특출나게 튀진 않지만, 어떤 상황에서도 기복 없이 안정적인 모습을 보여주어 주변 사람들에게 편안함을 줍니다. 다정하고 유쾌한 성격으로 누구와도 잘 어울리는 숨은 인싸이며, 결혼 상대로는 최고의 주가를 자랑하는 '현실 우량주' 타입입니다."}],
        "SGL": [
            {"name": "영수", "catchphrase": "기댈 수 있는 맏형! 지적인 중재자", "keywords": "#고민상담은나에게 #이과적해결법 #어른남자의매력 #나는중심을지킨다", "compatibility": {"best": "영숙 (YOL)", "worst": "영자 (YOC)"}, "description": "당신은 그룹의 중심을 잡아주는 '의젓한 리더' 타입입니다. 뛰어난 지성과 논리로 갈등 상황을 중재하고, 고민을 들어주며 든든한 해결책을 제시합니다. 섣불리 행동하기보다 신중하게 상황을 관망하며 최적의 수를 찾아내는 전략가입니다. 연장자다운 어른스러운 매력으로, 함께 있으면 안정감을 느끼게 해주는 사람입니다."},
            {"name": "영식", "catchphrase": "바른생활 테리우스! 젠틀한 모범생", "keywords": "#얼굴이개연성 #조용한강자 #젠틀함은기본 #알고보면순정파", "compatibility": {"best": "정숙 (YOC)", "worst": "순자 (YGL)"}, "description": "당신은 성실하고 건실한 '젠틀한 모범생' 타입입니다. 조용하지만 훈훈한 외모와 바른 인성으로 묵묵히 자신의 자리를 지키며 신뢰를 줍니다. 시끄러운 갈등을 싫어하며, 평화로운 관계를 선호해 나서는 일은 드물지만, 한번 마음을 연 상대에게는 누구보다 깊은 순정을 보여주는 '조용한 강자'입니다."}
        ]
    },
    "female": {
        "YOC": [
            {"name": "정숙", "catchphrase": "솔직함이 무기! 화끈한 맏언니", "keywords": "#돌려말하기는없다 #내가바로맏언니 #화끈한매력 #알고보면여린마음", "compatibility": {"best": "상철 (SOC)", "worst": "영수 (SGL)"}, "description": "당신은 돌려 말하기를 모르는 '솔직함의 화신'입니다. 자신의 감정과 생각을 필터 없이 표현하는 화끈한 매력을 가졌습니다. 그룹의 맏언니처럼 주변 사람들을 잘 챙기고 이끌어주는 리더십도 갖추고 있습니다. 때로 너무 솔직해서 미운 털이 박힐 때도 있지만, 뒤끝 없고 시원시원한 당신의 곁에는 항상 사람이 모입니다."},
            {"name": "영자", "catchphrase": "사랑과 눈물이 많은 귀염뽀짝 활력소", "keywords": "#인간이모티콘 #눈물버튼장착 #애교는나의힘 #귀여움한도초과", "compatibility": {"best": "영호 (YOC)", "worst": "현숙 (SGL)"}, "description": "당신은 감정이 얼굴에 그대로 드러나는 '인간 이모티콘'입니다. 작은 일에도 크게 웃고, 슬픈 영화를 보면 눈물을 펑펑 쏟는 순수한 감성의 소유자. 애교 넘치는 행동과 활발한 에너지로 주변에 활력을 불어넣는 귀염둥이. 감정 기복이 다소 있지만, 그 솔직하고 순수한 모습에 사람들은 무장해제됩니다."}
        ],
        "YOL": [{"name": "영숙", "catchphrase": "똑 부러진 매력! 할 말은 하는 알파걸", "keywords": "#내인생은내꺼 #강단있는여자 #팩트폭격기 #결혼은나처럼", "compatibility": {"best": "영수 (SGL)", "worst": "영호 (YOC)"}, "description": "당신은 자신의 주관이 뚜렷하고, 원하는 것을 쟁취할 줄 아는 '알파걸'입니다. 애매한 것을 싫어하며, 강단 있는 성격으로 자신의 의견을 솔직하게 표현합니다. 때로는 '기가 세다'는 오해를 받기도 하지만, 한번 맺은 인연은 소중히 여기는 따뜻한 마음을 가졌습니다. 능력과 생활력 모두 갖춘 당신은 어딜 가나 인정받는 사람입니다."}],
        "YGC": [], # 해당 유형 캐릭터 없음
        "YGL": [{"name": "순자", "catchphrase": "누구도 막을 수 없는 자유로운 영혼", "keywords": "#남시선은노상관 #마이웨이의아이콘 #자유로운영혼 #MZ대표", "compatibility": {"best": "상철 (SOC)", "worst": "영수 (SGL)"}, "description": "당신은 단체나 규칙에 얽매이는 것을 싫어하는 '자유로운 영혼'입니다. \"남들이 어떻게 생각하든 무슨 상관?\"이라며 자신의 길을 가는 '마이웨이의 아이콘'. 연애 전선에 뛰어들기보다는 자신의 감정과 자유를 더 중요하게 생각하며, 누구도 예측할 수 없는 방향으로 튀어 오르는 매력을 가졌습니다."}],
        "SOC": [{"name": "옥순", "catchphrase": "모두의 원픽! 매력의 중심", "keywords": "#가만히있어도인기폭발 #자체발광미모 #화제의중심 #알고보면철벽녀", "compatibility": {"best": "영철 (YOC)", "worst": "광수 (YGL)"}, "description": "당신은 특별히 노력하지 않아도 주변의 시선을 한 몸에 받는 '매력의 중심'입니다. 뛰어난 외모와 분위기로 첫인상에서 몰표를 받는 경우가 많으며, 모든 관계의 중심에서 이야기를 이끌어갑니다. 모두에게 친절하지만, 의외로 깐깐한 기준을 가지고 있어 쉽게 마음을 열지 않는 '알고 보면 철벽녀'의 매력도 가지고 있습니다."}],
        "SOL": [], # 해당 유형 캐릭터 없음
        "SGC": [], # 해당 유형 캐릭터 없음
        "SGL": [{"name": "현숙", "catchphrase": "보면 볼수록 매력적인 쿨뷰티", "keywords": "#차도녀인줄알았지? #알수록진국 #뇌섹녀 #감정보단논리", "compatibility": {"best": "광수 (YGL)", "worst": "영자 (YOC)"}, "description": "당신은 차갑고 시크한 첫인상 뒤에 깊은 매력을 숨기고 있는 '쿨뷰티' 타입입니다. 고스펙 '뇌섹녀'로, 감정보다는 이성적인 판단을 우선시합니다. 처음에는 다가가기 어렵다는 인상을 주지만, 시간이 지날수록 진국인 모습이 드러나는 '알수록 진국'인 사람. 당신의 진짜 매력을 알아보는 사람에게는 세상 가장 든든한 편이 되어줍니다."}],
    }
}
# YOL, YGC, SOL, SGC 유형에 남자 캐릭터가 없으므로 빈 리스트 추가
RESULTS["male"]["YOL"] = []
RESULTS["male"]["YGC"] = []
RESULTS["male"]["YGL"] = RESULTS["male"].get("YGL", []) # 이미 존재하면 그대로 사용
RESULTS["male"]["SOL"] = []
RESULTS["male"]["SGC"] = []

# 4. 유형 분석 및 결과 반환 API
@app.route('/calculate', methods=['POST', 'OPTIONS'])
def calculate():
    """사용자 답변을 받아 유형을 분석하고 결과를 JSON으로 반환합니다."""
    data = request.json
    answers = data.get('answers')
    gender = data.get('gender')

    if not answers or not gender or len(answers) != 6:
        return jsonify({"error": "Invalid request"}), 400

    # 유형 코드 계산
    type_counts = {'Y': 0, 'S': 0, 'O': 0, 'G': 0, 'C': 0, 'L': 0}
    type_map = {
        "1": {"A": "Y", "B": "S"}, "2": {"A": "Y", "B": "S"},
        "3": {"A": "O", "B": "G"}, "4": {"A": "O", "B": "G"},
        "5": {"A": "C", "B": "L"}, "6": {"A": "C", "B": "L"}
    }

    for i, ans in enumerate(answers, 1):
        question_num = str(i)
        type_code = type_map[question_num][ans]
        type_counts[type_code] += 1

    first_code = 'Y' if type_counts['Y'] >= type_counts['S'] else 'S'
    second_code = 'O' if type_counts['O'] >= type_counts['G'] else 'G'
    third_code = 'C' if type_counts['C'] >= type_counts['L'] else 'L'
    final_type = f"{first_code}{second_code}{third_code}"

    # 성별과 유형에 맞는 결과 캐릭터 선택
    possible_characters = RESULTS.get(gender, {}).get(final_type, [])

    if not possible_characters:
        # 매칭되는 캐릭터가 없는 경우, 가장 유사한 유형으로 대체 (예시 로직)
        # 실제 서비스에서는 이 부분을 더 정교하게 만들 수 있습니다.
        # 여기서는 가장 가까운 S/Y 유형의 기본 캐릭터를 반환하겠습니다.
        fallback_type = f"S{second_code}{third_code}" if first_code == 'Y' else f"Y{second_code}{third_code}"
        possible_characters = RESULTS.get(gender, {}).get(fallback_type, [])
        # 그래도 없으면 최종 fallback
        if not possible_characters:
            possible_characters = RESULTS.get(gender, {}).get("SOC", [])

    # 같은 유형에 여러 캐릭터가 있을 경우 랜덤으로 하나 선택
    result_character = random.choice(possible_characters)
    
    # 이미지 파일명 생성 (예: 영철 -> youngchul.png)
    name_en = {
        '영철': 'youngchul', '광수': 'gwangsu', '영수': 'youngsu', '상철': 'sangchul', '영호': 'youngho', '영식': 'youngsik',
        '옥순': 'oksun', '영숙': 'youngsook', '현숙': 'hyunsook', '정숙': 'jungsook', '순자': 'sunja', '영자': 'youngja'
    }
    result_character['image_url'] = f"static/img/{name_en.get(result_character['name'], 'default')}.png"

    return jsonify(result_character)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')