"""
VNA test suite — PUC_2.1 Power ON/OFF + Detail
"""


from core import testcase
from core.app_controller import AppController
from pages.main_page import MainPage


# ════════════════════════════════════════════════════════════════════════════
#  TC1 · PUC_2.1 · Normal · Bật VNA — full automation
# ════════════════════════════════════════════════════════════════════════════

@testcase
def test_vna_puc_2_1_0001(s2vna_ctrl: AppController, main_page: MainPage):
    """
    @test_id: test_vna_puc_2_1_0001
    @brief: Bật VNA — khởi động S2VNA, PC17, vào RF Test Set và kết nối

    @details: Verify toàn bộ luồng khởi động:
              S2VNA simulator lên trước, PC17 lên sau,
              điều hướng vào RF Test Set và đạt trạng thái Connected.

    @pre:- Máy tính đã cài S2VNA và PC17
         - Không có instance nào đang chạy trước khi test

    @test_procedure:
                    [code]
                        - Fixture s2vna_ctrl tự động khởi động S2VNA
                        - Fixture app_ctrl tự động khởi động PC17
                        - Fixture main_page tự động: Tools → RF Test Set
                          → System → Connect → Connection → đợi Connected
                        - Assert trạng thái Connected trên UI
                    [!code]

    @pass_criteria:- UI PC17 hiển thị trạng thái "Connected"
                   - Nút "Disconnect" xuất hiện và enabled

    @test_level: software
    @test_type: functional
    @execution_type: automatic
    @hw_depend: yes
    """
    # Fixtures đã xử lý toàn bộ luồng khởi động.
    # Test chỉ verify kết quả cuối.
    assert s2vna_ctrl.is_running(), "S2VNA chưa được khởi động — PC17 sẽ không thể Connected"
    assert main_page.is_connected(), "PC17 không đạt trạng thái 'Connected'"
    assert main_page.has_text("Disconnect"), "Nút 'Disconnect' không xuất hiện trên UI"
    main_page.click_detail()

    temperature = main_page.get_temperature()
    serial      = main_page.get_serial_number()

    errors = []
    if temperature in [None, "", ":"]:
        errors.append(f"Temperature không hợp lệ: {temperature!r}")
    if serial in [None, "", ":"]:
        errors.append(f"Serial Number không hợp lệ: {serial!r}")

    assert not errors, "\n".join(errors)



# ════════════════════════════════════════════════════════════════════════════
#  TC2 · PUC_2.1 · Abnormal · Bật/tắt liên tục VNA
# ════════════════════════════════════════════════════════════════════════════


@testcase
def test_vna_puc_2_1_0002(main_page: MainPage, device: SerialDevice):
    """
    @test_id: test_vna_puc_2_1_0002
    @brief: Bật/tắt liên tục VNA
    @details: Verify rằng VNA có thể bật/tắt liên tục 5 lần mà không bị lỗi,
              trạng thái phần cứng và UI phải đúng sau mỗi chu kỳ

    @pre:- PC17 application đang chạy
         - Module VNA đã bật (tiếp tục từ TC1 PUC_2.1 Normal)

    @test_procedure:
                    [code]
                        - Xác nhận thiết bị đã khởi động hoàn tất trên UI
                        - Tắt nguồn module VNA từ UI
                        - Quan sát đèn báo nguồn VNA và ghi nhận trạng thái UI
                        - Bật nguồn module VNA từ UI
                        - Quan sát đèn báo nguồn VNA và ghi nhận trạng thái khởi động thành công
                        - Lặp lại 5 lần
                    [!code]

    @pass_criteria:- Sau mỗi lần tắt: đèn VNA tắt, UI hiển thị OFF
                   - Sau mỗi lần bật: đèn VNA sáng, UI hiển thị ON/Ready
                   - Hoàn thành đủ 5 chu kỳ không có lỗi

    @test_level: software
    @test_type: functional
    @execution_type: Manual
    @hw_depend: yes
    """
   