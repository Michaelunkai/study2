class ChoicesController < ApplicationController
  before_action :set_choice, only: %i[ show edit update destroy ]

  # GET /choices or /choices.json
  def index
    @choices = Choice.all
  end

  # GET /choices/1 or /choices/1.json
  def show
  end

  # GET /choices/new
  def new
    @choice = Choice.new
  end

  # GET /choices/1/edit
  def edit
  end

  # POST /choices or /choices.json
  def create
    @choice = Choice.new(choice_params)

    respond_to do |format|
      if @choice.save
        format.html { redirect_to choice_url(@choice), notice: "Choice was successfully created." }
        format.json { render :show, status: :created, location: @choice }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @choice.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /choices/1 or /choices/1.json
  def update
    respond_to do |format|
      if @choice.update(choice_params)
        format.html { redirect_to choice_url(@choice), notice: "Choice was successfully updated." }
        format.json { render :show, status: :ok, location: @choice }
      else
        format.html { render :edit, status: :unprocessable_entity }
        format.json { render json: @choice.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /choices/1 or /choices/1.json
  def destroy
    @choice.destroy!

    respond_to do |format|
      format.html { redirect_to choices_url, notice: "Choice was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_choice
      @choice = Choice.find(params[:id])
    end

    # Only allow a list of trusted parameters through.
    def choice_params
      params.require(:choice).permit(:content, :question_id)
    end
end
