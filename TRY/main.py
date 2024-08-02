from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox 
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooser
import json
import os
import shutil

file_path = 'data/data.json' 
class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        

        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.username_input = TextInput(hint_text='Username', size_hint=(None, None), size=(300, 50))
        self.password_input = TextInput(hint_text='Password', password=True, size_hint=(None, None), size=(300, 50))
        self.login_button = Button(text='Login', size_hint=(None, None), size=(100, 50))
        self.login_button.bind(on_press=self.check_credentials)

        self.add_widget(Label(text='Welcome to the Si PaRi App', size_hint=(None, None), size=(300, 50), pos_hint={"center_x": 0.5}))
        self.add_widget(self.username_input)
        self.add_widget(self.password_input)
        self.add_widget(self.login_button)

    def check_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Add your authentication logic here
        if username == 'admin' and password == 'admin':
            self.show_popup("Login successful!")
        else:
            self.show_popup("Login failed!")

    def show_popup(self, message):
        popup = Popup(title='Login Status',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400,200))
        popup.open()
        self.clear_widgets()
        self.add_widget(MainMenu())
        
class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.company_data_button = Button(text='Company Data', size_hint=(None, None), size=(300, 50))
        self.document_submission_button = Button(text='Document Submission', size_hint=(None, None), size=(300, 50))
        self.document_review_button = Button(text='Document Review', size_hint=(None, None), size=(300, 50))
        self.document_guide_button = Button(text='Document Guide', size_hint=(None, None), size=(300, 50))
        self.logout_button = Button(text='Log Out', size_hint=(None, None), size=(300, 50))

        self.add_widget(self.company_data_button)
        self.add_widget(self.document_submission_button)
        self.add_widget(self.document_review_button)
        self.add_widget(self.document_guide_button)
        self.add_widget(self.logout_button)

        self.company_data_button.bind(on_press=self.show_company_data)
        self.document_submission_button.bind(on_press=self.show_document_submission)
        self.document_review_button.bind(on_press=self.show_document_review)
        self.document_guide_button.bind(on_press=self.show_document_guide)
        self.logout_button.bind(on_press=self.log_out)

    def show_company_data(self, instance):
        self.clear_widgets()
        self.add_widget(CompanyDataMenu())

    def show_document_submission(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentSubmissionMenu())

    def show_document_review(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentReviewMenu())    

    def show_document_guide(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentGuideMenu()) 
        
    def log_out(self, instance):
        self.clear_widgets()
        self.add_widget(LoginScreen())

class SelectableRecycleGridLayout(RecycleGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.default_size = None, 26
        self.default_size_hint = 1, None
        self.size_hint_y = None
        self.height = self.minimum_height
        self.orientation = 'tb-lr' #changed orientation to a valid option
        self.multiselect = True
        self.touch_multiselect = True

class SelectableButton(Button,ButtonBehavior):
    def __init__(self, data_items,**kwargs):
        super().__init__(**kwargs)
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)
    
    def on_touch_down(self, touch):
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            self.selected = not self.selected
            return True
        return False
    
    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

class MyRecycleView(RecycleView):
    def __init__(self, data_items,**kwargs):
        super().__init__(**kwargs)
        self.data = [{'text': str(x)} for x in data_items]
        self.viewclass = 'SelectableButton'
        self.layout_manager = SelectableRecycleGridLayout()
        
class CompanyDataMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.company_name_input = TextInput(hint_text='Company Name', size_hint=(None, None), size=(300, 50))
        self.business_type_input = TextInput(hint_text='Business Type', size_hint=(None, None), size=(300, 50))
        self.address_input = TextInput(hint_text='Address', size_hint=(None, None), size=(300, 50))
        self.responsible_name_input = TextInput(hint_text='Responsible Person Name', size_hint=(None, None), size=(300, 50))
        self.position_input = TextInput(hint_text='Position', size_hint=(None, None), size=(300, 50))
        self.email_input = TextInput(hint_text='Email', size_hint=(None, None), size=(300, 50))
        self.phone_number_input = TextInput(hint_text='Phone Number', size_hint=(None, None), size=(300, 50))

        self.save_button = Button(text='Save', size_hint=(None, None), size=(100, 50))
        self.save_button.bind(on_press=self.save_company_data)
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)

        self.add_widget(Label(text='Company Data', size_hint=(None, None), size=(300, 50), pos_hint={"center_x": 0.5}))
        self.add_widget(self.company_name_input)
        self.add_widget(self.business_type_input)
        self.add_widget(self.address_input)
        self.add_widget(self.responsible_name_input)
        self.add_widget(self.position_input)
        self.add_widget(self.email_input)
        self.add_widget(self.phone_number_input)
        self.add_widget(self.save_button)
        self.add_widget(self.back_button)

    def save_company_data(self, instance):
        company_name = self.company_name_input.text
        business_type = self.business_type_input.text
        address = self.address_input.text
        responsible_name = self.responsible_name_input.text
        position = self.position_input.text
        email = self.email_input.text
        phone_number = self.phone_number_input.text
        if os.path.exists(file_path):
            with open("data/company data.json","r") as file:
                data = json.load(file)
            obj = [
                {
                    "id":len(data) + 1,
                    "name":str(company_name),
                    "type":str(business_type),
                    "address":str(address),
                    "responsible_person":str(responsible_name),
                    "position":str(position),
                    "email":str(email),
                    "phone":str(phone_number)
                }
            ]
            data.extend(obj)
            with open("data/company data.json","w") as add:
                json.dump(data,add,indent=2)
        else:
            with open("data/company data.json","a") as createFile:
                createFile.read()
        # Add your logic to save company data here
        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.company_name_input = TextInput(hint_text="Company Name",size_hint=(None, None), size=(300, 50)) 
        print(f'Saving Company Data:\n Name - {company_name},\n Type - {business_type},\n Address - {address},\n Responsible Person - {responsible_name},\n Position - {position},\n Email - {email},\n Phone - {phone_number}')
                   
    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(MainMenu())

class DocumentSubmissionMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.technical_approval_button = Button(text='Technical Approval of Wastewater Utilization', size_hint=(None, None), size=(500, 50))
        self.hazardous_waste_button = Button(text='Technical Details of Hazardous Waste Storage', size_hint=(None, None), size=(500, 50))
        self.emission_disposal_button = Button(text='Technical Approval for Emission Disposal', size_hint=(None, None), size=(500, 50))
        self.wastewater_disposal_button = Button(text='Technical Approval for Wastewater Disposal', size_hint=(None, None), size=(500, 50))
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        
        self.add_widget(self.technical_approval_button)
        self.add_widget(self.hazardous_waste_button)
        self.add_widget(self.emission_disposal_button)
        self.add_widget(self.wastewater_disposal_button)
        self.add_widget(self.back_button)

        self.technical_approval_button.bind(on_press=self.submit_technical_approval)
        self.hazardous_waste_button.bind(on_press=self.submit_hazardous_waste)
        self.emission_disposal_button.bind(on_press=self.submit_emission_disposal)
        self.wastewater_disposal_button.bind(on_press=self.submit_wastewater_disposal)
        self.back_button.bind(on_press=self.go_back)

    def submit_technical_approval(self, instance):
        self.clear_widgets()
        self.add_widget(SubmitDocumentTechnicalUtilizationMenu())
   
    def submit_hazardous_waste(self, instance):
        self.clear_widgets()
        self.add_widget(SubmitDocumentTechnicalHazardousMenu())

    def submit_emission_disposal(self, instance):
        self.clear_widgets()
        self.add_widget(SubmitDocumentTechnicalEmissionMenu())

    def submit_wastewater_disposal(self, instance):
        self.clear_widgets()
        self.add_widget(SubmitDocumentTechnicalWastewaterMenu())
        
    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(MainMenu())

class DocumentReviewMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.review_technical_approval_button = Button(text='Review Technical Approval', size_hint=(None, None), size=(500, 50))
        self.review_technical_detail_button = Button(text='Review Technical Details', size_hint=(None, None), size=(500, 50))
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        
        self.add_widget(self.review_technical_approval_button)
        self.add_widget(self.review_technical_detail_button)
        self.add_widget(self.back_button)

        self.review_technical_approval_button.bind(on_press=self.show_review_technical_approval)
        self.review_technical_detail_button.bind(on_press=self.show_review_technical_detail)
        self.back_button.bind(on_press=self.go_back)

    def show_review_technical_approval(self, instance):
        self.clear_widgets()
        self.add_widget(ReviewTechnicalApprovalMenu())

    def show_review_technical_detail(self, instance):
        self.clear_widgets()
        self.add_widget(ReviewTechnicalDetailMenu())

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(MainMenu())

class DocumentGuideMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.guide_technical_approval_button = Button(text='Guide Technical Approval', size_hint=(None, None), size=(500, 50))
        self.guide_technical_detail_button = Button(text='Guide Technical Details', size_hint=(None, None), size=(500, 50))
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        
        self.add_widget(self.guide_technical_approval_button)
        self.add_widget(self.guide_technical_detail_button)
        self.add_widget(self.back_button)

        self.guide_technical_approval_button.bind(on_press=self.show_guide_technical_approval)
        self.guide_technical_detail_button.bind(on_press=self.show_guide_technical_detail)
        self.back_button.bind(on_press=self.go_back)

    def show_guide_technical_approval(self, instance):
        self.clear_widgets()
        self.add_widget(GuideTechnicalApprovalMenu())

    def show_guide_technical_detail(self, instance):
        self.clear_widgets()
        self.add_widget(GuideTechnicalDetailMenu())

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentGuideMenu())        

class GuideTechnicalApprovalMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.guide_technical_approval_button = Button(text='Guide Technical Approval', size_hint=(None, None), size=(500, 50))
        self.guide_technical_detail_button = Button(text='Guide Technical Details', size_hint=(None, None), size=(500, 50))
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        
        self.add_widget(self.guide_technical_approval_button)
        self.add_widget(self.guide_technical_detail_button)
        self.add_widget(self.back_button)

        self.guide_technical_approval_button.bind(on_press=self.show_guide_technical_approval)
        self.guide_technical_detail_button.bind(on_press=self.show_guide_technical_detail)
        self.back_button.bind(on_press=self.go_back)
    
    def go_back(self, instance):
            self.clear_widgets()
            self.add_widget(DocumentGuideMenu())

class GuideTechnicalDetailMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.guide_technical_detail_button = Button(text='Guide Technical Details', size_hint=(None, None), size=(500, 50))
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        
        self.add_widget(self.guide_technical_detail_button)
        self.add_widget(self.back_button)

        self.guide_technical_detail_button.bind(on_press=self.show_guide_technical_detail)
        self.back_button.bind(on_press=self.go_back)
    
    def go_back(self, instance):
            self.clear_widgets()
            self.add_widget(DocumentGuideMenu())

class SubmitDocumentTechnicalUtilizationMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.root = BoxLayout(orientation='vertical')

        # Label to display the selected file path
        self.file_label = Label(text="No file selected")
        self.root.add_widget(self.file_label)

        # Button to open the file chooser
        self.select_button = Button(text="Select File")
        self.select_button.bind(on_release=self.open_file_chooser)
        self.add_widget(self.select_button)    
        # TextInput to enter the destination folder
        self.destination_input = TextInput(hint_text="Enter destination folder", multiline=False)
        self.add_widget(self.destination_input)

        # Button to upload the selected file
        self.upload_button = Button(text="Upload File")
        self.upload_button.bind(on_release=self.upload_file)
        self.root.add_widget(self.upload_button)

        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)
        self.add_widget(self.back_button)

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        content.add_widget(filechooser)

        select_button = Button(text="Select")
        content.add_widget(select_button)

        popup = Popup(title="Select a file", content=content, size_hint=(0.9, 0.9))

        def select_file(instance):
            selected = filechooser.selection
            if selected:
                self.file_label.text = selected[0]
            popup.dismiss()

        select_button.bind(on_release=select_file)
        popup.open()

    def upload_file(self, instance):
        if not os.path.exists(destination_folder):
            self.show_message(f"Destination folder does not exist: {destination_folder}")
        file_path = self.file_label.text
        destination_folder = self.destination_input.text

        file_path = self.file_chooser.selection[0]
        file_name = file_path.split('/')[-1]
        print(f'File uploaded: {file_name}')

        if file_path != "No file selected" and destination_folder:
            try:
                shutil.copy(self.selected_file_path, destination_folder)
                self.file_label.text = "No file selected"
                self.destination_input.text = ""
                self.show_message("File uploaded successfully!")
            except Exception as e:
                self.show_message(f"Error: {e}")
        else:
            self.show_message("Please select a file and enter a destination folder.")

    def show_message(self, message):
        popup = Popup(title="Message", content=Label(text=message), size_hint=(0.8, 0.8))
        popup.open() 

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentSubmissionMenu())

class SubmitDocumentTechnicalHazardousMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.root = BoxLayout(orientation='vertical')

        # Label to display the selected file path
        self.file_label = Label(text="No file selected")
        self.root.add_widget(self.file_label)

        # Button to open the file chooser
        self.select_button = Button(text="Select File")
        self.select_button.bind(on_release=self.open_file_chooser)
        self.add_widget(self.select_button)    
        # TextInput to enter the destination folder
        self.destination_input = TextInput(hint_text="Enter destination folder", multiline=False)
        self.add_widget(self.destination_input)

        # Button to upload the selected file
        self.upload_button = Button(text="Upload File")
        self.upload_button.bind(on_release=self.upload_file)
        self.root.add_widget(self.upload_button)

        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)
        self.add_widget(self.back_button)

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        content.add_widget(filechooser)

        select_button = Button(text="Select")
        content.add_widget(select_button)

        popup = Popup(title="Select a file", content=content, size_hint=(0.9, 0.9))

        def select_file(instance):
            selected = filechooser.selection
            if selected:
                self.file_label.text = selected[0]
            popup.dismiss()

        select_button.bind(on_release=select_file)
        popup.open()

    def upload_file(self, instance):
        file_path = self.file_label.text
        destination_folder = self.destination_input.text

        if file_path != "No file selected" and destination_folder:
            try:
                shutil.copy(file_path, destination_folder)
                self.file_label.text = "No file selected"
                self.destination_input.text = ""
                self.show_message("File uploaded successfully!")
            except Exception as e:
                self.show_message(f"Error: {e}")
        else:
            self.show_message("Please select a file and enter a destination folder.")

        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)
        self.add_widget(self.back_button)

    def show_message(self, message):
        popup = Popup(title="Message", content=Label(text=message), size_hint=(0.8, 0.8))
        popup.open() 

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentSubmissionMenu())

class SubmitDocumentTechnicalEmissionMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.root = BoxLayout(orientation='vertical')

        # Label to display the selected file path
        self.file_label = Label(text="No file selected")
        self.root.add_widget(self.file_label)

        # Button to open the file chooser
        self.select_button = Button(text="Select File")
        self.select_button.bind(on_release=self.open_file_chooser)
        self.add_widget(self.select_button)    
        # TextInput to enter the destination folder
        self.destination_input = TextInput(hint_text="Enter destination folder", multiline=False)
        self.add_widget(self.destination_input)

        # Button to upload the selected file
        self.upload_button = Button(text="Upload File")
        self.upload_button.bind(on_release=self.upload_file)
        self.root.add_widget(self.upload_button)

        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)
        self.add_widget(self.back_button)

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        content.add_widget(filechooser)

        select_button = Button(text="Select")
        content.add_widget(select_button)

        popup = Popup(title="Select a file", content=content, size_hint=(0.9, 0.9))

        def select_file(instance):
            selected = filechooser.selection
            if selected:
                self.file_label.text = selected[0]
            popup.dismiss()

        select_button.bind(on_release=select_file)
        popup.open()

    def upload_file(self, instance):
        file_path = self.file_label.text
        destination_folder = self.destination_input.text

        if file_path != "No file selected" and destination_folder:
            try:
                shutil.copy(file_path, destination_folder)
                self.file_label.text = "No file selected"
                self.destination_input.text = ""
                self.show_message("File uploaded successfully!")
            except Exception as e:
                self.show_message(f"Error: {e}")
        else:
            self.show_message("Please select a file and enter a destination folder.")

    def show_message(self, message):
        popup = Popup(title="Message", content=Label(text=message), size_hint=(0.8, 0.8))
        popup.open() 

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentSubmissionMenu())

class SubmitDocumentTechnicalWastewaterMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.root = BoxLayout(orientation='vertical')

        # Label to display the selected file path
        self.file_label = Label(text="No file selected")
        self.root.add_widget(self.file_label)

        # Button to open the file chooser
        self.select_button = Button(text="Select File")
        self.select_button.bind(on_release=self.open_file_chooser)
        self.add_widget(self.select_button)    
        # TextInput to enter the destination folder
        self.destination_input = TextInput(hint_text="Enter destination folder", multiline=False)
        self.add_widget(self.destination_input)

        # Button to upload the selected file
        self.upload_button = Button(text="Upload File")
        self.upload_button.bind(on_release=self.upload_file)
        self.root.add_widget(self.upload_button)

        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)
        self.add_widget(self.back_button)

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        content.add_widget(filechooser)
        
        select_button = Button(text="Select")
        content.add_widget(select_button)

        popup = Popup(title="Select a file", content=content, size_hint=(0.9, 0.9))

        def select_file(instance):
            selected = filechooser.selection
            if selected:
                self.file_label.text = selected[0]
            popup.dismiss()

        select_button.bind(on_release=select_file)
        popup.open()

    def upload_file(self, instance):
        file_path = self.file_label.text
        destination_folder = self.destination_input.text

        if file_path != "No file selected" and destination_folder:
            try:
                shutil.copy(file_path, destination_folder)
                self.file_label.text = "No file selected"
                self.destination_input.text = ""
                self.show_message("File uploaded successfully!")
            except Exception as e:
                self.show_message(f"Error: {e}")
        else:
            self.show_message("Please select a file and enter a destination folder.")

    
    def show_message(self, message):
        popup = Popup(title="Message", content=Label(text=message), size_hint=(0.8, 0.8))
        popup.open() 

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentSubmissionMenu())

class ReviewTechnicalApprovalMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.checklist_button = Button(text='Checklist Technical Approval', size_hint=(None, None), size=(500, 50))
        self.baps_button = Button(text='BAPS', size_hint=(None, None), size=(500, 50))
        self.ba_improvement_button = Button(text='BA Improvement', size_hint=(None, None), size=(500, 50))
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        
        self.add_widget(self.checklist_button)
        self.add_widget(self.baps_button)
        self.add_widget(self.ba_improvement_button)
        self.add_widget(self.back_button)

        self.checklist_button.bind(on_press=self.show_checklist)
        self.baps_button.bind(on_press=self.show_baps)
        self.ba_improvement_button.bind(on_press=self.show_ba_improvement)
        self.back_button.bind(on_press=self.go_back)

    def show_checklist(self, instance):
        self.clear_widgets()
        self.add_widget(ChecklistMenu())

    def show_baps(self, instance):
        self.clear_widgets()
        self.add_widget(BAPSMenu())

    def show_ba_improvement(self, instance):
        self.clear_widgets()
        self.add_widget(BAImprovementMenu())

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentReviewMenu())

class ChecklistMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.checklist_technical_utilization_button = Button(text='Checklist Document Technical Utilization', size_hint=(None, None), size=(500, 50))
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        
        self.add_widget(self.checklist_technical_utilization_button)
        self.add_widget(self.back_button)

        self.checklist_technical_utilization_button.bind(on_press=self.show_checklist_technical_utilization)
        self.back_button.bind(on_press=self.go_back)

    def show_checklist_technical_utilization(self, instance):
        self.clear_widgets()
        self.add_widget(ChecklistDocumentTechnicalUtilizationMenu())

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentReviewMenu())

class ChecklistDocumentTechnicalUtilizationMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(ChecklistDocumentTechnicalUtilizationMenu, self).__init__(**kwargs)
        # Create a ScrollView to hold the list
        self.scrollview = ScrollView()
        self.add_widget(self.scrollview)

        # Create a BoxLayout to hold the list items
        self.list_layout = BoxLayout(orientation='vertical',size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scrollview.add_widget(self.list_layout)

        # Add list items
        self.add_list_item("Deskripsi Kegiatan","")
        self.add_list_item("1 Jenis dan Kapasitas Rencana Usaha dan/atau Kegiatan","")
        self.add_list_item("2) Jenis dan Jumlah Bahan Penolong yang Digunakan", "")
        self.add_list_item("3) Proses Usaha dan/atau Kegiatan yang Digunakan: a) Proses utama dan proses penunjang usaha dan/atau kegiatan secara keseluruhan", "")
        self.add_list_item("b) Persetujuan Teknis", "")
        self.add_list_item("c) Neraca air", "")
        self.add_list_item("d) Fluktuasi atau kontinuitas produksi dan Air Limbah: i) Lokasi: Sumur yang mewakili upstream dan downstream", "")
        self.add_list_item("ii) Parameter mutu air tanah", "")
        self.add_list_item("iii) Frekuensi pemantauan parameter air tanah yang dipantau pada sumur pantau", "")
        self.add_list_item("4) Efisiensi Penggunaan Air", "")
        self.add_list_item("Baku Mutu Air Limbah, Baku Mutu Air Limbah Nasional", "")
        self.add_list_item("Rencana Pengelolaan dan Pemantauan Lingkungan", "")
        self.add_list_item("Rencana Pengelolaan Lingkungan", "")
        self.add_list_item("Rencana Pemantauan Lingkungan", "")
        self.add_list_item("a) Pemantauan Air Limbah", "")
        self.add_list_item("i) Lokasi pengambilan contoh uji air limbah", "")
        self.add_list_item("ii) Mutu air limbah", "")
        self.add_list_item("iii) Dosis, debit dan rotasi untuk penyiraman atau volume air limbah yang digunakan untuk pencucian", "")
        self.add_list_item("iv) Frekuensi pemantauan disesuaikan dengan parameter yang dipantau", "")
        self.add_list_item("b)Pemantauan Mutu Air Tanah", "")
        self.add_list_item("i)Lokasi: sumur pantau yang mewakili hulu(upstream) dan hilir(downstream).", "") 
        self.add_list_item("ii)Parameter mutuair tanah", "")

        # Create a dictionary to store the checkbox data
        self.checkbox_data = {}

    def add_list_item(self, label_text, checkbox_text):
        # Create a horizontal BoxLayout to hold the label and checkbox
        item_layout = BoxLayout(orientation='horizontal')
        item_layout.size_hint_y = None
        item_layout.height = 355
        self.list_layout.add_widget(item_layout)

        # Create a Label
        label = Label(text=label_text, size_hint_x=None, size_hint_y=None,
            height=100,
            font_size=20,
            text_size=(self.width, None),
            valign='top',
            )
        item_layout.add_widget(label)

        # Create a CheckBox
        checkbox = CheckBox(size_hint=(0.2, 0.2))
        item_layout.add_widget(checkbox)

        # Create a Label to display the checkbox text
        checkbox_label = Label(text=checkbox_text, size_hint_x=1)
        item_layout.add_widget(checkbox_label)


class ReviewTechnicalDetailMenu(BoxLayout): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.checklistd_button = Button(text='Checklist Technical Detail', size_hint=(None, None), size=(500, 50))
        self.ba_verification_button = Button(text='BA of Field Verification', size_hint=(None, None), size=(500, 50))
        self.ba_improvement_button = Button(text='BA Improvement', size_hint=(None, None), size=(500, 50))
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        
        self.add_widget(self.checklistd_button)
        self.add_widget(self.ba_verification_button)
        self.add_widget(self.ba_improvement_button)
        self.add_widget(self.back_button)

        self.checklistd_button.bind(on_press=self.show_checklistd)
        self.ba_verification_button.bind(on_press=self.show_ba_verification)
        self.ba_improvement_button.bind(on_press=self.show_ba_improvement)
        self.back_button.bind(on_press=self.go_back)

    def show_checklistd(self, instance):
        self.clear_widgets()
        self.add_widget(ChecklistTechnicalDetailMenu())

    def show_ba_verification(self, instance):
        self.clear_widgets()
        self.add_widget(BAofFieldVerificationMenu())

    def show_ba_improvement(self, instance):
        self.clear_widgets()
        self.add_widget(BAImprovementMenu())

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentReviewMenu())

class ChecklistTechnicalDetailMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(ChecklistTechnicalDetailMenu, self).__init__(**kwargs)
        # Create a ScrollView to hold the list
        self.scrollview = ScrollView()
        self.add_widget(self.scrollview)

        # Create a BoxLayout to hold the list items
        self.list_layout = BoxLayout(orientation='vertical',size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scrollview.add_widget(self.list_layout)

        # Add list items
        self.add_list_item("Deskripsi Kegiatan","")
        self.add_list_item("1 Jenis dan Kapasitas Rencana Usaha dan/atau Kegiatan","")
        self.add_list_item("2) Jenis dan Jumlah Bahan Penolong yang Digunakan", "")
        self.add_list_item("3) Proses Usaha dan/atau Kegiatan yang Digunakan: a) Proses utama dan proses penunjang usaha dan/atau kegiatan secara keseluruhan", "")
        self.add_list_item("b) Persetujuan Teknis", "")
        self.add_list_item("c) Neraca air", "")
        self.add_list_item("d) Fluktuasi atau kontinuitas produksi dan Air Limbah: i) Lokasi: Sumur yang mewakili upstream dan downstream", "")
        self.add_list_item("ii) Parameter mutu air tanah", "")
        self.add_list_item("iii) Frekuensi pemantauan parameter air tanah yang dipantau pada sumur pantau", "")
        self.add_list_item("4) Efisiensi Penggunaan Air", "")
        self.add_list_item("Baku Mutu Air Limbah, Baku Mutu Air Limbah Nasional", "")
        self.add_list_item("Rencana Pengelolaan dan Pemantauan Lingkungan", "")
        self.add_list_item("Rencana Pengelolaan Lingkungan", "")
        self.add_list_item("Rencana Pemantauan Lingkungan", "")
        self.add_list_item("a) Pemantauan Air Limbah", "")
        self.add_list_item("i) Lokasi pengambilan contoh uji air limbah", "")
        self.add_list_item("ii) Mutu air limbah", "")
        self.add_list_item("iii) Dosis, debit dan rotasi untuk penyiraman atau volume air limbah yang digunakan untuk pencucian", "")
        self.add_list_item("iv) Frekuensi pemantauan disesuaikan dengan parameter yang dipantau", "")
        self.add_list_item("b)Pemantauan Mutu Air Tanah", "")
        self.add_list_item("i)Lokasi: sumur pantau yang mewakili hulu(upstream) dan hilir(downstream).", "") 
        self.add_list_item("ii)Parameter mutuair tanah", "")

        # Create a dictionary to store the checkbox data
        self.checkbox_data = {}

    def add_list_item(self, label_text, checkbox_text):
        # Create a horizontal BoxLayout to hold the label and checkbox
        item_layout = BoxLayout(orientation='horizontal')
        item_layout.size_hint_y = None
        item_layout.height = 355
        self.list_layout.add_widget(item_layout)

        # Create a Label
        label = Label(text=label_text, size_hint_x=0.2, size_hint_y=None,
            height=100,
            font_size=20,
            text_size=(self.width, None),
            valign='top',
            )
        item_layout.add_widget(label)

        # Create a CheckBox
        checkbox = CheckBox()
        item_layout.add_widget(checkbox)

        # Create a Label to display the checkbox text
        checkbox_label = Label(text=checkbox_text, size_hint_x=1)
        item_layout.add_widget(checkbox_label)


class BAPSMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.waktu_pelaksanaan_input = TextInput(hint_text='Waktu Pelaksanaan', size_hint=(None, None), size=(300, 50))
        self.nama_input = TextInput(hint_text='Nama', size_hint=(None, None), size=(300, 50))
        self.instansi_input = TextInput(hint_text='Instansi', size_hint=(None, None), size=(300, 50))
        self.nip_input = TextInput(hint_text='NIP', size_hint=(None, None), size=(300, 50))
        self.jabatan_input = TextInput(hint_text='Jabatan', size_hint=(None, None), size=(300, 50))
        self.dihadiri_oleh_input = TextInput(hint_text='Dihadiri Oleh', size_hint=(None, None), size=(300, 50))
        self.berdasarkan_dokumen_standar_teknis_input = TextInput(hint_text='Berdasarkan Dokumen Standar Teknis', size_hint=(None, None), size=(300, 50))
        self.tindak_lanjut_input = TextInput(hint_text='Tindak Lanjut', size_hint=(None, None), size=(300, 50))

        self.save_button = Button(text='Save', size_hint=(None, None), size=(100, 50))
        self.save_button.bind(on_press=self.save_BAPS)
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)

        self.add_widget(Label(text='BAPS', size_hint=(None, None), size=(300, 50), pos_hint={"center_x": 0.5}))
        self.add_widget(self.waktu_pelaksanaan_input)
        self.add_widget(self.nama_input)
        self.add_widget(self.instansi_input)
        self.add_widget(self.nip_input)
        self.add_widget(self.jabatan_input)
        self.add_widget(self.dihadiri_oleh_input)
        self.add_widget(self.berdasarkan_dokumen_standar_teknis_input)
        self.add_widget(self.tindak_lanjut_input)
        self.add_widget(self.save_button)
        self.add_widget(self.back_button)

    def save_BAPS(self, instance):
        waktu_pelaksanaan = self.waktu_pelaksanaan_input.text
        nama = self.nama_input.text
        nip = self.nip_input.text
        jabatan = self.jabatan_input.text
        dihadiri_oleh = self.dihadiri_oleh_input.text
        berdasarkan_dokumen_standar_teknis = self.berdasarkan_dokumen_standar_teknis_input.text
        tindak_lanjut = self.tindak_lanjut_input.text
        if os.path.exists(file_path):
            with open("data/BAPS data.json","r") as file:
                data = json.load(file)
            obj = [
                {
                    "id":len(data) + 1,
                    "waktu_pelaksanaan":str(waktu_pelaksanaan),
                    "nama":str(nama),
                    "nip":str(nip),
                    "jabatan":str(jabatan),
                    "dihadiri_oleh":str(dihadiri_oleh),
                    "berdasarkan_dokumen_standar_teknis":str(berdasarkan_dokumen_standar_teknis),
                    "tindak_lanjut":str(tindak_lanjut)
                }
            ]
            data.extend(obj)
            with open("data/BAPS data.json","w") as add:
                json.dump(data,add,indent=2)
        else:
            with open("data/BAPS data.json","a") as createFile:
                createFile.read()
        # Add your logic to save company data here
        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        # Add your logic to save BAPS here
        print(f'Saving BAPS:\n Waktu Pelaksanaan - {waktu_pelaksanaan},\n Nama - {nama}, NIP - {nip},\n Jabatan - {jabatan},\n Dihadiri Oleh - {dihadiri_oleh},\n Berdasarkan Dokumen Standar Teknis - {berdasarkan_dokumen_standar_teknis},\n Tindak Lanjut - {tindak_lanjut}')

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentReviewMenu)

class BAImprovementMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.waktu_pelaksanaan_input = TextInput(hint_text='Waktu Pelaksanaan', size_hint=(None, None), size=(300, 50))
        self.nama_input = TextInput(hint_text='Nama', size_hint=(None, None), size=(300, 50))
        self.instansi_input = TextInput(hint_text='Instansi', size_hint=(None, None), size=(300, 50))
        self.nip_input = TextInput(hint_text='NIP', size_hint=(None, None), size=(300, 50))
        self.jabatan_input = TextInput(hint_text='Jabatan', size_hint=(None, None), size=(300, 50))
        self.dihadiri_oleh_input = TextInput(hint_text='Dihadiri Oleh', size_hint=(None, None), size=(300, 50))
        self.berdasarkan_dokumen_standar_teknis_input = TextInput(hint_text='Berdasarkan Dokumen Standar Teknis', size_hint=(None, None), size=(300, 50))
        self.tindak_lanjut_input = TextInput(hint_text='Tindak Lanjut', size_hint=(None, None), size=(300, 50))

        self.save_button = Button(text='Save', size_hint=(None, None), size=(100, 50))
        self.save_button.bind(on_press=self.save_BAPS)
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)

        self.add_widget(Label(text='BAPT', size_hint=(None, None), size=(300, 50), pos_hint={"center_x": 0.5}))
        self.add_widget(self.waktu_pelaksanaan_input)
        self.add_widget(self.nama_input)
        self.add_widget(self.instansi_input)
        self.add_widget(self.nip_input)
        self.add_widget(self.jabatan_input)
        self.add_widget(self.dihadiri_oleh_input)
        self.add_widget(self.berdasarkan_dokumen_standar_teknis_input)
        self.add_widget(self.tindak_lanjut_input)
        self.add_widget(self.save_button)
        self.add_widget(self.back_button)

    def save_BAPT(self, instance):
        waktu_pelaksanaan = self.waktu_pelaksanaan_input.text
        nama = self.nama_input.text
        nip = self.nip_input.text
        jabatan = self.jabatan_input.text
        dihadiri_oleh = self.dihadiri_oleh_input.text
        berdasarkan_dokumen_standar_teknis = self.berdasarkan_dokumen_standar_teknis_input.text
        tindak_lanjut = self.tindak_lanjut_input.text

        # Add your logic to save BAPT here
        print(f'Saving BAPT:\n Waktu Pelaksanaan - {waktu_pelaksanaan},\n Nama - {nama}, NIP - {nip},\n Jabatan - {jabatan},\n Dihadiri Oleh - {dihadiri_oleh},\n Berdasarkan Dokumen Standar Teknis - {berdasarkan_dokumen_standar_teknis},\n Tindak Lanjut - {tindak_lanjut}')

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentReviewMenu)

class BAPSMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.waktu_pelaksanaan_input = TextInput(hint_text='Waktu Pelaksanaan', size_hint=(None, None), size=(300, 50))
        self.nama_input = TextInput(hint_text='Nama', size_hint=(None, None), size=(300, 50))
        self.instansi_input = TextInput(hint_text='Instansi', size_hint=(None, None), size=(300, 50))
        self.nip_input = TextInput(hint_text='NIP', size_hint=(None, None), size=(300, 50))
        self.jabatan_input = TextInput(hint_text='Jabatan', size_hint=(None, None), size=(300, 50))
        self.dihadiri_oleh_input = TextInput(hint_text='Dihadiri Oleh', size_hint=(None, None), size=(300, 50))
        self.berdasarkan_dokumen_standar_teknis_input = TextInput(hint_text='Berdasarkan Dokumen Standar Teknis', size_hint=(None, None), size=(300, 50))
        self.tindak_lanjut_input = TextInput(hint_text='Tindak Lanjut', size_hint=(None, None), size=(300, 50))

        self.save_button = Button(text='Save', size_hint=(None, None), size=(100, 50))
        self.save_button.bind(on_press=self.save_BAPS)
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)

        self.add_widget(Label(text='BAPS', size_hint=(None, None), size=(300, 50), pos_hint={"center_x": 0.5}))
        self.add_widget(self.waktu_pelaksanaan_input)
        self.add_widget(self.nama_input)
        self.add_widget(self.instansi_input)
        self.add_widget(self.nip_input)
        self.add_widget(self.jabatan_input)
        self.add_widget(self.dihadiri_oleh_input)
        self.add_widget(self.berdasarkan_dokumen_standar_teknis_input)
        self.add_widget(self.tindak_lanjut_input)
        self.add_widget(self.save_button)
        self.add_widget(self.back_button)

    def save_BAPS(self, instance):
        waktu_pelaksanaan = self.waktu_pelaksanaan_input.text
        nama = self.nama_input.text
        nip = self.nip_input.text
        jabatan = self.jabatan_input.text
        dihadiri_oleh = self.dihadiri_oleh_input.text
        berdasarkan_dokumen_standar_teknis = self.berdasarkan_dokumen_standar_teknis_input.text
        tindak_lanjut = self.tindak_lanjut_input.text
        if os.path.exists(file_path):
            with open("data/BAPS data.json","r") as file:
                data = json.load(file)
        obj = [{
            "id":len(data) + 1,
            "waktu pelaksanaan":str(waktu_pelaksanaan),
            "nama":str(nama),
            "nip":str(nip),
            "jabatan":str(jabatan),
            "dihadiri_oleh":str(dihadiri_oleh),
            "berdasarkan_dokumen_standar_teknis":str(berdasarkan_dokumen_standar_teknis),
            "tindak_lanjut":str(tindak_lanjut)
        }]
        data.extend(obj)
        with open("data/BAPS data.json","w") as add:
            json.dump(data,add,indent=2)
        # Add your logic to save BAPS here
        print(f'Saving BAPS:\n Waktu Pelaksanaan - {waktu_pelaksanaan},\n Nama - {nama}, NIP - {nip},\n Jabatan - {jabatan},\n Dihadiri Oleh - {dihadiri_oleh},\n Berdasarkan Dokumen Standar Teknis - {berdasarkan_dokumen_standar_teknis},\n Tindak Lanjut - {tindak_lanjut}')

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentReviewMenu())

class BAImprovementMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.waktu_pelaksanaan_input = TextInput(hint_text='Waktu Pelaksanaan', size_hint=(None, None), size=(300, 50))
        self.nama_input = TextInput(hint_text='Nama', size_hint=(None, None), size=(300, 50))
        self.instansi_input = TextInput(hint_text='Instansi', size_hint=(None, None), size=(300, 50))
        self.nip_input = TextInput(hint_text='NIP', size_hint=(None, None), size=(300, 50))
        self.jabatan_input = TextInput(hint_text='Jabatan', size_hint=(None, None), size=(300, 50))
        self.dihadiri_oleh_input = TextInput(hint_text='Dihadiri Oleh', size_hint=(None, None), size=(300, 50))
        self.berdasarkan_dokumen_standar_teknis_input = TextInput(hint_text='Berdasarkan Dokumen Standar Teknis', size_hint=(None, None), size=(300, 50))
        self.tindak_lanjut_input = TextInput(hint_text='Tindak Lanjut', size_hint=(None, None), size=(300, 50))

        self.save_button = Button(text='Save', size_hint=(None, None), size=(100, 50))
        self.save_button.bind(on_press=self.save_BAImprovementMenu)
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)

        self.add_widget(Label(text='BA Improvement', size_hint=(None, None), size=(300, 50), pos_hint={"center_x": 0.5}))
        self.add_widget(self.waktu_pelaksanaan_input)
        self.add_widget(self.nama_input)
        self.add_widget(self.instansi_input)
        self.add_widget(self.nip_input)
        self.add_widget(self.jabatan_input)
        self.add_widget(self.dihadiri_oleh_input)
        self.add_widget(self.berdasarkan_dokumen_standar_teknis_input)
        self.add_widget(self.tindak_lanjut_input)
        self.add_widget(self.save_button)
        self.add_widget(self.back_button)

    def save_BAImprovementMenu(self, instance):
        waktu_pelaksanaan = self.waktu_pelaksanaan_input.text
        nama = self.nama_input.text
        nip = self.nip_input.text
        jabatan = self.jabatan_input.text
        dihadiri_oleh = self.dihadiri_oleh_input.text
        berdasarkan_dokumen_standar_teknis = self.berdasarkan_dokumen_standar_teknis_input.text
        tindak_lanjut = self.tindak_lanjut_input.text
        if os.path.exists(file_path):
            with open("data/BAImprovement.json","r") as file:
                data = json.load(file)
        obj = [{
            "id":len(data) + 1,
            "waktu pelaksanaan":str(waktu_pelaksanaan),
            "nama":str(nama),
            "nip":str(nip),
            "jabatan":str(jabatan),
            "dihadiri_oleh":str(dihadiri_oleh),
            "berdasarkan_dokumen_standar_teknis":str(berdasarkan_dokumen_standar_teknis),
            "tindak_lanjut":str(tindak_lanjut)
        }]
        data.extend(obj)
        with open("data/BAImprovement.json","w") as add:
            json.dump(data,add,indent=2)
        # Add your logic to save BAImprovement here
        print(f'Saving BAImprovement:\n Waktu Pelaksanaan - {waktu_pelaksanaan},\n Nama - {nama}, NIP - {nip},\n Jabatan - {jabatan},\n Dihadiri Oleh - {dihadiri_oleh},\n Berdasarkan Dokumen Standar Teknis - {berdasarkan_dokumen_standar_teknis},\n Tindak Lanjut - {tindak_lanjut}')

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentReviewMenu)        

class BAofFieldVerificationMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = [50, 20]
        self.spacing = 20
        self.size_hint = (None, None)
        self.size = (400, 400)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        
        self.lampiran_berita_acara_input = TextInput(hint_text='Lampiran Berita Acara', size_hint=(None, None), size=(300, 50))
        self.waktu_pelaksanaan_input = TextInput(hint_text='Waktu Pelaksanaan', size_hint=(None, None), size=(300, 50))
        self.nama_input = TextInput(hint_text='Nama', size_hint=(None, None), size=(300, 50))
        self.instansi_input = TextInput(hint_text='Instansi', size_hint=(None, None), size=(300, 50))
        self.nip_input = TextInput(hint_text='NIP', size_hint=(None, None), size=(300, 50))
        self.golongan_input = TextInput(hint_text='Golongan', size_hint=(None, None), size=(300, 50))
        self.jabatan_input = TextInput(hint_text='Jabatan', size_hint=(None, None), size=(300, 50))
        self.dihadiri_oleh_input = TextInput(hint_text='Dihadiri Oleh', size_hint=(None, None), size=(300, 50))
        self.kesimpulan_input = TextInput(hint_text='Kesimpulan', size_hint=(None, None), size=(300, 50))

        self.save_button = Button(text='Save', size_hint=(None, None), size=(100, 50))
        self.save_button.bind(on_press=self.save_BAofFieldVerificationMenu)
        self.back_button = Button(text='Back', size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.go_back)

        self.add_widget(Label(text='BAofFieldVerificationMenu', size_hint=(None, None), size=(300, 50), pos_hint={"center_x": 0.5}))
        self.add_widget(self.waktu_pelaksanaan_input)
        self.add_widget(self.nama_input)
        self.add_widget(self.instansi_input)
        self.add_widget(self.nip_input)
        self.add_widget(self.golongan_input)
        self.add_widget(self.jabatan_input)
        self.add_widget(self.dihadiri_oleh_input)
        self.add_widget(self.kesimpulan_input)
        self.add_widget(self.save_button)
        self.add_widget(self.back_button)

    def save_BAofFieldVerificationMenu(self, instance):
        waktu_pelaksanaan = self.waktu_pelaksanaan_input.text
        nama = self.nama_input.text
        instansi = self.instansi_input.text
        nip = self.nip_input.text
        golongan = self.golongan_input.text
        jabatan = self.jabatan_input.text
        dihadiri_oleh = self.dihadiri_oleh_input.text
        kesimpulan = self.kesimpulan_input.text
        if os.path.exists(file_path):
            with open("data/BAofVerify.json","r") as file:
                data = json.load(file)
        obj = [{
            "id":len(data) + 1,
            "instansi":str(instansi),
            "nama":str(nama),
            "nip":str(nip),
            "golongan":str(golongan),
            "jabatan":str(jabatan),
            "dihadiri_oleh":str(dihadiri_oleh),
            "kesimpulan":str(kesimpulan)
        }]
        data.extend(obj)
        with open("data/BAofVerify.json","w") as add:
            json.dump(data,add,indent=2)
        # Add your logic to save BAofFieldVerificationMenu here
        print(f'Saving BA of Field Verification:\n Waktu Pelaksanaan - {waktu_pelaksanaan},\n Nama - {nama}, NIP - {nip},\n Golongan - {golongan},\n Jabatan - {jabatan},\n Dihadiri Oleh - {dihadiri_oleh},\n Kesimpulan - {kesimpulan}')

    def go_back(self, instance):
        self.clear_widgets()
        self.add_widget(DocumentReviewMenu())

class SIPaRiApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    SIPaRiApp().run()
