import java.io.File;

 final int image_height = 100;
 final int image_width = 100;

 File dir = new File("Documents/Processing/normalize_images/data_set/cropped");
 File[] files = dir.listFiles();
 
 String path;
 PImage final_blended_img = createImage(image_height, image_width, RGB);
 
 //BLEND (nah)
 //ADD (X)
 //SUBTRACT (X)
 //DARKEST (X)
 //LIGHTEST (eh)
 //DIFFERENCE (cool)
 //EXCLUSION (X)
 //MULTIPLY (X)
 //SCREEN (X)
 //OVERLAY (X)
 //HARD_LIGHT (eh)
 //SOFT_LIGHT (X)
 //DODGE (X)
 //BURN (X)
 
 for( int i=0; i < files.length; i++ ){ 
 
   path = files[i].getAbsolutePath();
   
   if( path.toLowerCase().endsWith(".png") ) {
     
       //resize
       String new_name = "data_set/normalized/nimg_" + i + ".png";
       PImage cur_img = loadImage( path );
       cur_img.resize(image_height, image_width);
       cur_img.save(new_name);
       
       //blend
       final_blended_img.blend(cur_img, 0, 0, image_width, image_height, 0, 0, image_width, image_height, DIFFERENCE);
       
       //***TMP*** check out intermideate steps ***TMP***
       String test_step_name = "data_set/test/step_" + i + ".png";
       final_blended_img.save(test_step_name);
   }
 }


//save final blendend image
final_blended_img.save("data_set/final.png");