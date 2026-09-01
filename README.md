# 오늘의 근력루틴 - 재구축 버전

## 포함된 페이지
- `index.html` : 홈
- `1rm-calculator.html` : 1RM 계산기 (Epley 공식)
- `strength-standards.html` : 체중/성별 기반 강도 표준표 (스쿼트/벤치/데드리프트)
- `workout-log.html` : localStorage 기반 운동 기록장
- `privacy.html` : 개인정보처리방침 (애드센스 심사 필수)

## 배포 방법 (GitHub Pages)
1. GitHub에서 새 저장소 생성 (예: `strength-routine-site`), Public으로 설정
2. 이 폴더의 파일 전체를 저장소에 업로드
   - github.dev (`https://github.dev/[계정]/[저장소명]`) 접속 후 파일 탐색기에 드래그 앤 드롭
   - 또는 github.com 저장소 페이지 → "Add file" → "Upload files" 로 전체 폴더 드래그
3. 저장소 Settings → Pages → Branch를 `main` / `(root)`로 설정 → Save
4. 1~2분 후 `https://[계정].github.io/[저장소명]/` 에서 확인

## 애드센스 관련 필수 체크
- `ca-pub-8486360926248718` 게시자 ID가 모든 페이지 `<head>`에 이미 삽입되어 있습니다.
- **ads.txt는 이 저장소가 아니라 루트 저장소(`[계정].github.io`)에 있어야** 인식됩니다. 이미 주방시간 사이트용으로 등록되어 있다면 추가 작업 불필요.
- `data-ad-slot="0000000000"` 은 임시값입니다. 애드센스 승인 후 실제 슬롯 ID로 교체하세요.
- 심사 신청 전 Google Search Console에 사이트 등록 및 sitemap 제출 권장.

## 추가 페이지(운동별 상세 가이드 등) 확장 방법
현재는 핵심 인터랙티브 기능 중심으로 4개 페이지를 구성했습니다.
운동별 상세 페이지(예: 벤치프레스 방법, 스쿼트 자세 교정 등)를 추가하려면
같은 `css/style.css`, `js/common.js`, 상단/하단 네비게이션 구조를 그대로 복사해
새 HTML 파일만 늘리면 됩니다. 페이지 수가 많아지면 데이터/템플릿 분리형
Python 빌드 스크립트(주방시간 사이트와 동일한 방식) 도입을 추천합니다.
