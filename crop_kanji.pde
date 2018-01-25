import java.io.File;

PImage src;
ArrayList<PImage> cropped_imgs = new ArrayList<PImage>();

//don't touch
int w_init = 41;
int h_init = 40;
int w_offset = 134;
int h_offset = 134;
int w_cur = w_init;
int h_cur = h_init;

void setup() {

  size(50,50);
  frameRate(24);
  
  //originals path = "Documents/Processing/crop_kanji/kanji_photos/originals/GET_FOLDER_NAME;
  //make cropped folder
  //cropped path = "Documents/Processing/crop_kanji/kanji_photos/FOLDER_NAME_HERE/CROPPED_IMAGES_HERE;
  
  //for each folder in orginals
  
  //resize source
  src = loadImage( "Documents/Processing/crop_kanji/kanji_photos/originals/sun/sun1_cropped.JPG" );
  src.resize(400,940);
  
  PImage cur_img;
  for(int i=1; i < 22; i++){
    
    cur_img = src.get(w_cur,h_cur,50,50);
    cropped_imgs.add(cur_img);
    
    /////////save cropped image with new_name
    //String path = Documents/Processing/crop_kanji/kanji_photos/cropped/"+ FOLDERNAME + "/";
    //String new_name = "FOLDERNAME_cropped_i.JPG";
    //cur_img.save(new_name);
    
    //***TMP***
    //project relative path unforunatley
    String path = "kanji_photos/cropped/sun/";
    String new_name = "sun_cropped_" + (i + 21) + ".JPG";
    cur_img.save(path + new_name);
    
    h_cur += h_offset;
    
    if(i%7 ==0){
      h_cur = h_init;
      w_cur += w_offset;
    }
  }
  
}

//test
int pos = 0;
void draw(){
  
    PImage cur_img = cropped_imgs.get(pos);
    image(cur_img, 0 ,0);
    
    pos++;
    if(pos >= cropped_imgs.size()){
      pos = 0;
    }
}