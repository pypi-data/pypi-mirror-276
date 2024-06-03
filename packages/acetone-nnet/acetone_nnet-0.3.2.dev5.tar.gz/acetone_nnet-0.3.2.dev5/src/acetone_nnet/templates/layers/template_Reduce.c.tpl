    // {{name}}_{{idx}}{{comment}}
    {{#all}}
    {{#Other}}
    reduced = {{starting_value}};
    
    {{/Other}}
    for (k = 0; k < {{size}}; ++k)
    {
        {{#Max}}
        if ({{output_str}}[k] > reduced)
        {
            reduced = {{output_str}}[k];
        }
        {{/Max}}
        {{#Min}}
        if ({{output_str}}[k] < reduced)
        {
            reduced = {{output_str}}[k];
        }
        {{/Min}}
        {{#Other}}
        reduced {{func}}= {{output_str}}[k];
        {{/Other}}
    }
    {{#Mean}}
    reduced = reduced/{{size}};
    {{/Mean}}

    output_{{road}}[0] = {{{activation_function}}};
    {{/all}}
    {{#two}}
    for (f = 0; f < {{output_dimension}}; ++f)
    {
        {{#Other}}
        tensor_temp[f] = {{starting_value}};

        {{/Other}}
        for (i = 0; i < {{reduced_dimension_1}}; ++i)
        {
            for (j = 0; j < {{reduced_dimension_2}}; ++j)
            {
                {{#Max}}
                if (output_{{road}}[{{position}}] > output_{{road}}[f])
                {
                    tensor_temp[f] = {{output_str}}[{{position}}];
                }
                {{/Max}}
                {{#Min}}
                if (output_{{road}}[{{position}}] < output_{{road}}[f])
                {
                    tensor_temp[f] = {{output_str}}[{{position}}];
                }
                {{/Min}}
                {{#Other}}
                tensor_temp[f] {{func}}= {{output_str}}[{{position}}];
                {{/Other}}
            }
        }
        {{#Avg}}
        tensor_temp[f] = tensor_temp[f]/{{size}};
        {{/Avg}}
    }

    for (k = 0; k < {{size}}; ++k)
    {
        output_{{road}}[k] = {{{activation_function}}};
    }
    {{/two}}
    {{#one}}
    for (f = 0; f < {{output_dimension_1}}; ++f)
    {
        for (i = 0; i < {{output_dimension_2}}; ++i)
        {
            {{#Other}}
            tensor_temp[{{position_1}}] = {{starting_value}};

            {{/Other}}
            for (j = 0; j < {{reduced_dimension}}; ++j)
            {
                {{#Max}}
                if ({{output_str}}[{{position_2}}] > tensor_temp[{{position_1}}])
                {
                    tensor_temp[{{position_1}}] = {{output_str}}[{{position_2}}];
                }
                {{/Max}}
                {{#Min}}
                if ({{output_str}}[{{position_2}}] < tensor_temp[{{position_1}}])
                {
                    tensor_temp[{{position_1}}] = {{output_str}}[{{position_2}}];
                }
                {{/Min}}
                {{#Other}}
                tensor_temp[{{position_1}}] {{func}}= {{output_str}}[{{position_2}}];
                {{/Other}}
            }
            {{#Avg}}
            tensor_temp[{{position_1}}] = tensor_temp[{{position_1}}]/{{size}};
            {{/Avg}}
        }
    }
    
    for (k = 0; k < {{size}}; ++k)
    {
        output_{{road}}[k] = {{{activation_function}}};
    }
    {{/one}}
    {{#none}}
    //Act like a Linear layer
    {{#Activation}}
    for (k = 0; k < {{size}}; ++k)
    {
        output_{{road}}[k] = {{{activation_functions}}};
    }
    {{/Activation}}
    {{/none}}