############################## 시각화 ###################################
import matplotlib.pyplot as plt
import cv2

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

def draw_and_save_image(model, img_path, save_path):
    # 이미지 불러오기
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV에서 matplotlib으로 이미지 포맷 변경

    # 추론 실행
    results = model(img)
    results.render()  # 결과 렌더링

    # 결과 이미지를 matplotlib으로 출력
    plt.figure(figsize=(10, 8))
    plt.imshow(results.ims[0])  # 결과 이미지 출력
    plt.axis('off')
    plt.title('YOLOv5 Detection Result')
    plt.show()

    # 결과 이미지 저장
    cv2.imwrite(save_path, cv2.cvtColor(results.ims[0], cv2.COLOR_RGB2BGR))
    print(f"이미지가 {save_path} 경로에 저장되었습니다.")


def draw_bar_chart(total_calory, total_carbon, total_protein, total_fat, total_natrium):
    # 각 카테고리별 색상 지정
    colors = ['orange', '#0047AB']

    # 서브플롯 생성 (5행 1열)
    fig, axs = plt.subplots(5, 1, figsize=(10, 8))

    # 데이터 리스트
    data = [
        (2500, total_calory, '칼로리(kcal)'),
        (300, total_carbon, '탄수화물(g)'),
        (60, total_protein, '단백질(g)'),
        (50, total_fat, '지방(g)'),
        (1500, total_natrium, '나트륨(mg)')
    ]

    # 각 서브플롯에 가로 바 차트 그리기
    for i, (recommended, consumed, label) in enumerate(data):
        bars = axs[i].barh(['권장', '섭취'], [recommended, consumed], color=colors, edgecolor='black')

        # 바 레이블 추가
        for bar in bars:
            # x 축 범위의 너비 계산
            x_width = axs[i].get_xlim()[1] - axs[i].get_xlim()[0]
            text_x = bar.get_width() + 0.03 * x_width
            axs[i].text(text_x, bar.get_y() + bar.get_height() / 2,
                        f'{int(bar.get_width())}', ha='center', va='center', color='black', fontsize=12
                        )

        axs[i].set_xlim(0, max(recommended, consumed) * 1.2)  # x축 범위 설정
        axs[i].set_ylabel(label, fontsize=14)
        axs[i].grid(True, axis='x', linestyle='--', alpha=0.7)
        axs[i].set_yticklabels(['권장', '섭취'], fontsize=12)

    # 메인 타이틀 추가
    fig.suptitle('영양소 섭취 분석', fontsize=20)

    # 전체 레이아웃 조정
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    return fig  # 그래프 객체 반환




