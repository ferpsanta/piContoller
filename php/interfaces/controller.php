<?php
interface Controller
{
    /**
     * @param  array  $input  The request parameters/data
     * @return mixed  The (userialized) return data
     */
    public function execute($input);
}
?>