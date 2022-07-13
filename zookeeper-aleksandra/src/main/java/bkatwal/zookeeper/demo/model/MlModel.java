package bkatwal.zookeeper.demo.model;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public class MlModel {

    public MlModel()
    {

    }

    private int id;
    private String modelName;
    private String guid;
    private String modelPath;
    private float accuracy;
    private float auc;

}