package bkatwal.zookeeper.demo.util; 

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;

import bkatwal.zookeeper.demo.model.MlModel;
import org.apache.tomcat.util.http.fileupload.FileUtils;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

public final class FileStorage
{
    private static String folderPathRoot = Paths.get("").toAbsolutePath().toString()+ "/uploads/";
    public static String folderPath  = "";
    private static List<MlModel> modelsList = new ArrayList<>();
    private static int globalId = 0;

    public static void createDir(String folderName)
    {
        folderName = folderName.replace(":", "-");
        folderPath = folderPathRoot +folderName +"/";

        try
        {
            Path path = Paths.get(folderPath);
            Files.createDirectories(path);
            System.out.println("Directory is created!");
        }
        catch (IOException e)
        {
            System.err.println("Failed to create directory!" +e.getMessage());
        }
    }

    public static List<MlModel> addFiles(List<MlModel> models)
    {
        for (MlModel model : models)
        {
            String filePath = folderPath;
            System.out.println("destin"+filePath);
            System.out.println("(********************************************************)");

            Path currentRelativePath = Paths.get("");
            String s = currentRelativePath.toAbsolutePath().toString()+"/pythonApp/"+model.getModelPath();

            System.out.println("copy"+s);
            StringBuilder contentBuilder = new StringBuilder();

            Path copied = Paths.get(folderPath+"/"+model.getGuid()+".h5");
            Path originalPath = Paths.get(s);

            try {
                Files.copy(originalPath, copied, StandardCopyOption.REPLACE_EXISTING);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

            MlModel modelForInsert = new MlModel(globalId, model.getModelName(), model.getGuid(), copied.toString() , model.getAccuracy(), model.getAuc() );
            globalId++;

            modelsList.add(modelForInsert);
        }
        return  modelsList;
    }

    public static List<MlModel> getModelsFromStorage() { return modelsList;}


    public static String updateFile(MultipartFile file, int id, boolean isMaster)
    {

        try {
            MlModel modelToChange = modelsList.get(id);

            System.out.println(modelToChange.getModelPath() + "********************************* model path");
            File file2 = new File(modelToChange.getModelPath());

            try {
                file.transferTo(file2);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

            if (isMaster)
            {
                System.out.println("**************promena putanje u globalnom dir *****************");
                //ako je master treba promeniti i u globalnoj bazi
                Path currentRelativePath = Paths.get("");
                String s = currentRelativePath.toAbsolutePath().toString()+"/pythonApp/models/"+modelToChange.getGuid()+".h5";
                File file3 = new File(s);

                try {
                    file.transferTo(file2);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }

            }
            return "SUCCESS";
        } catch ( IndexOutOfBoundsException e ) {
            return "No model with id="+id;
        }
    }

    private FileStorage() {}


//    __________________________________ kod sa casa ____________________________________________________________

    public static void deleteDir(String folderName)
    {
        folderPath = folderPathRoot +folderName +"/";

        try
        {
            FileUtils.forceDelete(new File(folderPath));
        }
        catch (IOException e)
        {
            System.out.println("Failed to delete directory " +folderPath +".\n" +e.getMessage());
        }
    }

//
//    public static FileModel GetFile(String fileName)
//    {
//        String filePath = folderPath +fileName;
//        StringBuilder contentBuilder = new StringBuilder();
//
//        try (Stream<String> stream = Files.lines(Paths.get(filePath), StandardCharsets.UTF_8))
//        {
//            stream.forEach(s -> contentBuilder.append(s).append("\n"));
//        }
//        catch (IOException e)
//        {
//            // e.printStrackTrace();
//        }
//
//        FileModel fm = new FileModel(globalId++, fileName, filePath, contentBuilder.toString());
//        return  fm;
//    }


    public static List<String> getFileNames()
    {
        List<String> fileNames = new ArrayList<>();
        File directoryPath = new File(folderPath);
        String contents[] = directoryPath.list();

        for (int i = 0; i < contents.length; i++)
            fileNames.add(contents[i]);
        
        return fileNames;
    }



}