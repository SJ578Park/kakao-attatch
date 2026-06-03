# References

## 주요 reference

- `silver-flight-group/kakaocli`
  - <https://github.com/silver-flight-group/kakaocli>
  - 목적: macOS용 KakaoTalk CLI. local SQLCipher DB read와 macOS Accessibility 기반 UI action을 다룹니다.
  - 중요 제한: macOS only.

## Crypto / database reference

- `sqlcipher/sqlcipher`
  - <https://github.com/sqlcipher/sqlcipher>
  - 목적: SQLite-compatible encrypted database library.
  - 관련성: `kakaocli`가 KakaoTalk encrypted local DB를 열 때 SQLCipher를 사용합니다.

## Key derivation reference

- blluv KakaoTalk Mac DB derivation gist
  - <https://gist.github.com/blluv/8418e3ef4f4aa86004657ea524f2de14>
  - 관련성: local `kakaocli` source comments가 database name과 key derivation의 근거로 이 gist를 언급합니다.

## Windows research references

- Kakao DevTalk thread mentioning Windows local KakaoTalk user data path
  - <https://devtalk.kakao.com/t/pc-chat-data/116661>
  - 관련성: `%localappdata%\Kakao\KakaoTalk\users\<hash>\` 같은 path를 언급합니다.

- DFRWS paper on encrypted DB files in Windows messengers
  - <https://dfrws.org/sites/default/files/session-files/2019_EU_paper-digital_forensic_analysis_of_encrypted_database_files_in_instant_messaging_applications_on_windows_operating_systems_case_study_with_kakaotalk_nateon_and_qq_messenger.pdf>
  - 관련성: Windows KakaoTalk historical forensic reference입니다. 현재 Windows client가 같은 방식으로 동작한다는 증거로 보면 안 됩니다.

## Notes

이 reference들은 공개 가능한 구현 계획 참고용입니다. KakaoTalk terms, local laws, user consent requirements를 지켜야 합니다.

English summary: These references support public documentation and implementation planning only. They do not grant permission to collect third-party data or bypass KakaoTalk terms, laws, or consent requirements.
