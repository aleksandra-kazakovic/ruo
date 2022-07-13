package bkatwal.zookeeper.demo.controller;

import static bkatwal.zookeeper.demo.util.ZkDemoUtil.getHostPostOfServer;
import static bkatwal.zookeeper.demo.util.ZkDemoUtil.isEmpty;

import bkatwal.zookeeper.demo.model.MlModel;
import bkatwal.zookeeper.demo.model.Person;
import bkatwal.zookeeper.demo.util.ClusterInfo;


import java.util.List;
import javax.servlet.http.HttpServletRequest;

import bkatwal.zookeeper.demo.util.DataStorage;
import bkatwal.zookeeper.demo.util.FileStorage;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

/** @author "Bikas Katwal" 26/03/19 */
@RestController
public class ZookeeperDemoController {

  private RestTemplate restTemplate = new RestTemplate();
  private static String hostname = "http://127.0.0.1:5000/";
  private static String mlPredict = "predict";
  private static String mlSummary = "modelSummary";


  @GetMapping("/models")
  public ResponseEntity<List<MlModel>> getModels() {
    List<MlModel> models = FileStorage.getModelsFromStorage();
      return ResponseEntity.ok(models);

  }

  @PostMapping("/updateModel")
  public  ResponseEntity<String>  updateModel(
          HttpServletRequest request,
          @RequestParam("file") MultipartFile file,
          @RequestParam("id") Integer id)
  {
    String requestFrom = request.getHeader("request_from");
    String leader = ClusterInfo.getClusterInfo().getMaster();

    if (!isEmpty(requestFrom) && requestFrom.equalsIgnoreCase(leader) && !amILeader()) {
      //System.out.println("Lider naredio promenu request from: "+requestFrom+" ________________lideer je "+leader);
      FileStorage.updateFile(file,id, false);
      return ResponseEntity.ok("SUCCESS");
    }

    if (amILeader()) {
      //System.out.println("Lider dobio zahtev------------------------");
      List<String> liveNodes = ClusterInfo.getClusterInfo().getLiveNodes();
      int successCount = 0;
      for (String node : liveNodes) {

        if (getHostPostOfServer().equals(node)) {
          //System.out.println("Lider menja svoje-------------------------");
          FileStorage.updateFile(file,id, true);
          successCount++;
        } else { //lider salje zahtev ostalima da odrade
          //System.out.println("Lider sprema zahtev drugom nodu-------------------------");
          String requestUrl =
                  "http://"
                          .concat(node)
                          .concat("updateModel");
          HttpHeaders headers = new HttpHeaders();
          headers.add("request_from", leader);
          headers.setContentType(MediaType.MULTIPART_FORM_DATA);

          MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();

          body.add("file", file.getResource());
          body.add("id", id);

          HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
          restTemplate.postForEntity(requestUrl, requestEntity, byte[].class);

          headers.setContentType(MediaType.APPLICATION_JSON);

          successCount++;
        }
      }
      return ResponseEntity.ok()
              .body("Successfully update ".concat(String.valueOf(successCount)).concat(" nodes"));
    } else {
      //saljemo lideru da izvrsi
      //System.out.println("Nisam lider i prosledjujem njemu-------------------------");
      String requestUrl =
              "http://"
                      .concat(leader)
                      .concat("updateModel");
      HttpHeaders headers = new HttpHeaders();
      headers.add("request_from", leader);
      headers.setContentType(MediaType.MULTIPART_FORM_DATA);

      MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();

      body.add("file", file.getResource());
      body.add("id", id);

      HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
      return restTemplate.postForEntity(requestUrl, requestEntity, String.class);
    }
  }

  @PostMapping("/predict")
  public  ResponseEntity<String>  predict(
          HttpServletRequest request,
          @RequestParam("file") MultipartFile file,
          @RequestParam("id") Integer id)
  {

    List<MlModel> modelsList = FileStorage.getModelsFromStorage();

    try {
      MlModel modelToPredict = modelsList.get(id);

      String requestUrl = hostname + mlPredict;
      HttpHeaders headers = new HttpHeaders();
      headers.setContentType(MediaType.MULTIPART_FORM_DATA);
      MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();

      body.add("file", file.getResource());
      body.add("model_guid", modelToPredict.getGuid());

      HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
      ResponseEntity<String> response = restTemplate.postForEntity(requestUrl, requestEntity, String.class);

      return ResponseEntity.ok(response.getBody());

    } catch ( IndexOutOfBoundsException e ) {
      return ResponseEntity.ok("No models with id = "+id.toString()+". Total models: "+modelsList.toArray().length+". ");
    }
  }

  @PostMapping("/modelSummary")
  public  ResponseEntity<String>  modelSummary(
          HttpServletRequest request,
          @RequestParam("id") Integer id)
  {

    List<MlModel> modelsList = FileStorage.getModelsFromStorage();

    try {
      MlModel modelToPredict = modelsList.get(id);

      String requestUrl = hostname + mlSummary;
      HttpHeaders headers = new HttpHeaders();
      headers.setContentType(MediaType.MULTIPART_FORM_DATA);
      MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
      body.add("file_path", modelToPredict.getModelPath());

      HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
      ResponseEntity<String> response = restTemplate.postForEntity(requestUrl, requestEntity, String.class);

      return ResponseEntity.ok(response.getBody());

    } catch ( IndexOutOfBoundsException e ) {
      return ResponseEntity.ok("No models with id = "+id.toString()+". Total models: "+modelsList.toArray().length+". ");
    }
  }





  // ----------------------------------- primer sa casa ----------------------------------------------------------------------------

/*
Primer sa casa ****************
  @PutMapping("/savefile/{filename}/{contents}")
  public ResponseEntity<String> saveFile(
          HttpServletRequest request,
          @PathVariable("filename") String filename,
          @PathVariable("contents") String contents)
  {
    String requestFrom = request.getHeader("request_from");
    String leader = ClusterInfo.getClusterInfo().getMaster();

    if (!isEmpty(requestFrom) && requestFrom.equalsIgnoreCase(leader)) {
      FileStorage.PutFile(filename, contents);
      return ResponseEntity.ok("SUCCESS");
    }

    if (amILeader()) {
      List<String> liveNodes = ClusterInfo.getClusterInfo().getLiveNodes();
      int successCount = 0;
      for (String node : liveNodes) {

        if (getHostPostOfServer().equals(node)) {
          FileStorage.PutFile(filename, contents);
          successCount++;
        } else {
          String requestUrl =
                  "http://"
                          .concat(node)
                          .concat("savefile")
                          .concat("/")
                          .concat(filename)
                          .concat("/")
                          .concat(contents);
          HttpHeaders headers = new HttpHeaders();
          headers.add("request_from", leader);
          headers.setContentType(MediaType.APPLICATION_JSON);

          HttpEntity<String> entity = new HttpEntity<>(headers);
          restTemplate.exchange(requestUrl, HttpMethod.PUT, entity, String.class).getBody();
          successCount++;
        }
      }

      return ResponseEntity.ok()
              .body("Successfully update ".concat(String.valueOf(successCount)).concat(" nodes"));
    } else {
      String requestUrl =
              "http://"
                      .concat(leader)
                      .concat("savefile")
                      .concat("/")
                      .concat(filename)
                      .concat("/")
                      .concat(contents);
      HttpHeaders headers = new HttpHeaders();

      headers.setContentType(MediaType.APPLICATION_JSON);

      HttpEntity<String> entity = new HttpEntity<>(headers);
      return restTemplate.exchange(requestUrl, HttpMethod.PUT, entity, String.class);
    }
  }


  @PutMapping("/person/{id}/{name}")
  public ResponseEntity<String> savePerson(
      HttpServletRequest request,
      @PathVariable("id") Integer id,
      @PathVariable("name") String name) {

    String requestFrom = request.getHeader("request_from");
    String leader = ClusterInfo.getClusterInfo().getMaster();
    if (!isEmpty(requestFrom) && requestFrom.equalsIgnoreCase(leader)) {
      Person person = new Person(id, name);
      DataStorage.setPerson(person);
      return ResponseEntity.ok("SUCCESS");
    }
    // If I am leader I will broadcast data to all live node, else forward request to leader
    if (amILeader()) {
      List<String> liveNodes = ClusterInfo.getClusterInfo().getLiveNodes();

      int successCount = 0;
      for (String node : liveNodes) {

        if (getHostPostOfServer().equals(node)) {
          Person person = new Person(id, name);
          DataStorage.setPerson(person);
          successCount++;
        } else {
          String requestUrl =
              "http://"
                  .concat(node)
                  .concat("person")
                  .concat("/")
                  .concat(String.valueOf(id))
                  .concat("/")
                  .concat(name);
          HttpHeaders headers = new HttpHeaders();
          headers.add("request_from", leader);
          headers.setContentType(MediaType.APPLICATION_JSON);

          HttpEntity<String> entity = new HttpEntity<>(headers);
          restTemplate.exchange(requestUrl, HttpMethod.PUT, entity, String.class).getBody();
          successCount++;
        }
      }

      return ResponseEntity.ok()
          .body("Successfully update ".concat(String.valueOf(successCount)).concat(" nodes"));
    } else {
      String requestUrl =
          "http://"
              .concat(leader)
              .concat("person")
              .concat("/")
              .concat(String.valueOf(id))
              .concat("/")
              .concat(name);
      HttpHeaders headers = new HttpHeaders();

      headers.setContentType(MediaType.APPLICATION_JSON);

      HttpEntity<String> entity = new HttpEntity<>(headers);
      return restTemplate.exchange(requestUrl, HttpMethod.PUT, entity, String.class);
    }
  }
*/
  private boolean amILeader() {
    String leader = ClusterInfo.getClusterInfo().getMaster();
    return getHostPostOfServer().equals(leader);
  }


//  @GetMapping("/persons")
//  public ResponseEntity<List<Person>> getPerson() {
//
//    return ResponseEntity.ok(DataStorage.getPersonListFromStorage());
//  }

  @GetMapping("/clusterInfo")
  public ResponseEntity<ClusterInfo> getClusterinfo() {

    return ResponseEntity.ok(ClusterInfo.getClusterInfo());
  }
}
