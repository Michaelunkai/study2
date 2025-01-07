require "application_system_test_case"

class ChoicesTest < ApplicationSystemTestCase
  setup do
    @choice = choices(:one)
  end

  test "visiting the index" do
    visit choices_url
    assert_selector "h1", text: "Choices"
  end

  test "should create choice" do
    visit choices_url
    click_on "New choice"

    fill_in "Content", with: @choice.content
    fill_in "Question", with: @choice.question_id
    click_on "Create Choice"

    assert_text "Choice was successfully created"
    click_on "Back"
  end

  test "should update Choice" do
    visit choice_url(@choice)
    click_on "Edit this choice", match: :first

    fill_in "Content", with: @choice.content
    fill_in "Question", with: @choice.question_id
    click_on "Update Choice"

    assert_text "Choice was successfully updated"
    click_on "Back"
  end

  test "should destroy Choice" do
    visit choice_url(@choice)
    click_on "Destroy this choice", match: :first

    assert_text "Choice was successfully destroyed"
  end
end
