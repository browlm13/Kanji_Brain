/*
                                    Pixel Array Data Generator
 
 input dir: "original_photos"
 input files: photos from template sheets. cropped to specified dots. (names = PHOTONAME_ITERATION#.JPG)
 applied changes: crop, white/black, reduced size.
 saves formated images for error checking into "error_ckecking" dir (names: PHOTONAME_PAGE#_BOX/IMAGE#.JPG)
 creates: "pixel_array_data.txt"
 
 */

import java.io.File;

//settings
final int IMG_HEIGHT = 10;
final int IMG_WIDTH = 10;
final float CONTRAST_CONST = .5;
final int FRAME_RATE = 120;

//file and dir names
final String training_data_file_name = "pixel_array_data.txt";
final String original_photos_dir_name = "original_photos";
final String error_ckecking_dir_name = "error_ckecking";

//paths
final String project_path_name = "Documents/Processing/pixel_array_data_gen/";
String training_set_path_name =  project_path_name + original_photos_dir_name;
String error_checking_path_name = error_ckecking_dir_name + "/";

///////////////////////////////  program  ///////////////////////////////

//dirs
File training_set_dir = new File(training_set_path_name);

//mass pixel data
ArrayList<String> mass_pixel_data = new ArrayList<String>();

//arrray of high contrast images for error checking
ArrayList<PImage> high_contrast_imgs = new ArrayList<PImage>();

//functions
String get_photo_name(File original_photo) {
  //format: PHOTONAME_PAGE#.JPG -> extract: PHOTONAME
  String file_path = original_photo.getAbsolutePath();
  String[] all_folder_names = split(file_path.toString(), '/');
  String file_name = new String(all_folder_names[all_folder_names.length - 1]);
  String[] file_name_info = split(file_name.toString(), '_');
  String photo_name = file_name_info[0];
  return photo_name;
}

int get_photo_page_number(File original_photo) {
  //format: PHOTONAME_PAGE#.JPG -> extract: PAGE#
  String file_path = original_photo.getAbsolutePath();
  String[] all_folder_names = split(file_path.toString(), '/');
  String file_name = new String(all_folder_names[all_folder_names.length - 1]);
  String[] file_name_info = split(file_name.toString(), '_');
  //remove ending
  String[] ending_and_page_number = split(file_name_info[1].toString(), '0'); 
  int page_number = int(ending_and_page_number[0]);
  return page_number;
}

//get new photo pixel array values
ArrayList<Integer> get_pixel_array(PImage photo) {
  //returns new array of values for image (values 0 or 255)

  ArrayList<Integer> pixel_array = new ArrayList<Integer>();
  float gray_scale_value;
  int pixel_value;

  photo.loadPixels();

  for (int j=0; j < photo.pixels.length; j++) {

    /*
             get color and convert to value between 0 and 1
     formula: (r + g + b) / (255 + 255 + 255)
     then convert value to 0 or 255 (0 if > CONTRAST_CONST)
     */

    //convert to grayscale
    gray_scale_value = (red(photo.pixels[j]) + green(photo.pixels[j]) + green(photo.pixels[j]))/765;

    //max contrast
    if (gray_scale_value > CONTRAST_CONST)
    { 
      pixel_value = 255;
    } else
    { 
      pixel_value = 0;
    }

    //add to pixel array
    pixel_array.add(pixel_value);
  }

  return pixel_array;
}

//crop images and return image array
ArrayList<PImage> get_cropped_imgs_array(PImage original) {

  //arrray of cropped images
  ArrayList<PImage> cropped_imgs = new ArrayList<PImage>();

  //don't touch
  int w_init = 41;
  int h_init = 40;
  int w_offset = 134;
  int h_offset = 134;
  int w_cur = w_init;
  int h_cur = h_init;

  //resize source
  original.resize(400, 940);

  PImage cur_img;
  for (int i=1; i < 22; i++) {

    cur_img = original.get(w_cur, h_cur, 50, 50);  //why are these hard codded???
    cropped_imgs.add(cur_img);

    h_cur += h_offset;

    if (i%7 ==0) {
      h_cur = h_init;
      w_cur += w_offset;
    }
  }

  return cropped_imgs;
}

//add to pixel array data
void add_data(String photo_name, ArrayList<Integer> pixel_array) {

  String new_data = photo_name;
  for (int i=0; i < pixel_array.size(); i++) {
    new_data +=  " " + pixel_array.get(i);
  }

  mass_pixel_data.add(new_data);
}

//update pixels
PImage update_pixels(PImage img, ArrayList<Integer> new_pixel_array) {

  img.loadPixels();
  for (int i = 0; i < img.pixels.length; i++) {
    int pix_val = new_pixel_array.get(i);
    img.pixels[i] = color(pix_val, pix_val, pix_val); 
  }
  img.updatePixels();

  return img;
}


//build error checking image array and save file
void error_checking(String photo_name, int page_num, int block_num, PImage img) {
  high_contrast_imgs.add(img);
  String new_photo_name = photo_name + "_" + page_num + "_" + block_num + ".JPG";
  img.save(error_checking_path_name + new_photo_name);
}


void setup() {
  size(10, 10);
  frameRate(FRAME_RATE);


  //program execute
  File[] original_photos = training_set_dir.listFiles();


  for (int i=0; i < original_photos.length; i++) {

    if ((!original_photos[i].toString().endsWith(".DS_Store")) && (original_photos[i].toString().endsWith(".JPG"))) {

      PImage cur_photo = loadImage(original_photos[i].toString());

      //crop_img
      ArrayList<PImage> cropped_imgs = get_cropped_imgs_array(cur_photo);
      String photo_name = get_photo_name(original_photos[i]);
      int page_num = get_photo_page_number(original_photos[i]);
      int block_num;


      for (int j=0; j < cropped_imgs.size(); j++) {

        PImage cur_img = cropped_imgs.get(j);
        block_num = j;

        //resize image
        cur_img.resize(IMG_HEIGHT, IMG_WIDTH);

        //get pixel array of high contrast image
        ArrayList<Integer> pixel_array = get_pixel_array(cur_img);

        //make image high contrast
        cur_img = update_pixels(cur_img, pixel_array); 

        //add data to mass array
        add_data(photo_name, pixel_array);

        //build error checking array and save file
        error_checking(photo_name, page_num, block_num, cur_img);
      }
    }
  }

   //save training data file with all image data
   String[] buffer = new String[mass_pixel_data.size()];
   for(int i=0;i<mass_pixel_data.size();i++){buffer[i] = mass_pixel_data.get(i);}
   saveStrings(training_data_file_name, buffer);

} 

//cycles through error visulization array images
int pos = 0;
void draw() {

   PImage cur_img = high_contrast_imgs.get(pos);
   image(cur_img, 0 ,0);
   
   pos++;
   if(pos >= high_contrast_imgs.size()){
     pos = 0;
   }
}  