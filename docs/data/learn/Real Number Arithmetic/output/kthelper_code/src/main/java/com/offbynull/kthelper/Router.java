package com.offbynull.kthelper;

import static java.nio.charset.StandardCharsets.UTF_8;
import java.nio.file.Files;
import java.nio.file.Path;
import static java.util.stream.Collectors.joining;

public class Router {
    public static void main(String[] args) throws Exception {
        var lines = Files.readAllLines(Path.of("/input/input.data"), UTF_8);
        var routeTo = lines.get(0);
        var actualInput = lines.stream().skip(1L).collect(joining("\n"));
        
        var cls = Router.class.getClassLoader().loadClass(
                Router.class.getPackageName() + "." +routeTo
        );
        var output = (String) cls.getMethod("run", String.class).invoke(null, actualInput);
        Files.writeString(Path.of("/output/output.md"), output, UTF_8);
    }
    
}
